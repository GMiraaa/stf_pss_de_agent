import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

const PARTICIPANT_ID = 'stf-de-agent.de';
const API_BASE = 'http://127.0.0.1:8765';
const SERVER_PORT = 8765;
const STARTUP_TIMEOUT_MS = 20_000;

let serverProcess: cp.ChildProcess | null = null;

// ---------------------------------------------------------------------------
// Utilitários
// ---------------------------------------------------------------------------

function getWorkspaceRoot(): string | undefined {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
}

/** Prefere o Python do venv local, senão cai no python3 do PATH. */
function getPythonPath(workspaceRoot: string): string {
    const candidates = [
        path.join(workspaceRoot, '.venv', 'bin', 'python'),
        path.join(workspaceRoot, 'venv', 'bin', 'python'),
    ];
    for (const p of candidates) {
        if (fs.existsSync(p)) { return p; }
    }
    return 'python3';
}

/** Executa um comando e aguarda a conclusão. Rejeita se o exit code != 0. */
function runCommand(cmd: string, args: string[], cwd: string): Promise<void> {
    return new Promise((resolve, reject) => {
        const proc = cp.spawn(cmd, args, { cwd });
        proc.on('exit', (code) => (code === 0 ? resolve() : reject(new Error(`exit ${code}`))));
        proc.on('error', reject);
    });
}

/** Fica tentando o /health até o servidor responder ou o timeout estourar. */
async function waitForServer(): Promise<boolean> {
    const deadline = Date.now() + STARTUP_TIMEOUT_MS;
    while (Date.now() < deadline) {
        try {
            const res = await fetch(`${API_BASE}/health`);
            if (res.ok) { return true; }
        } catch { /* ainda não está pronto */ }
        await new Promise(r => setTimeout(r, 500));
    }
    return false;
}

// ---------------------------------------------------------------------------
// Ciclo de vida do servidor
// ---------------------------------------------------------------------------

async function startServer(stream: vscode.ChatResponseStream): Promise<void> {
    // Verifica se já está rodando
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            stream.markdown('Servidor já está em execução. Pode conversar!');
            return;
        }
    } catch { /* não está rodando */ }

    const workspaceRoot = getWorkspaceRoot();
    if (!workspaceRoot) {
        stream.markdown('Nenhum workspace aberto.');
        return;
    }

    const python = getPythonPath(workspaceRoot);

    // 1. Instalar dependências
    stream.markdown('**[1/2]** Instalando dependências (`pip install -r requirements.txt`)…');
    try {
        await runCommand(python, ['-m', 'pip', 'install', '-r', 'requirements.txt', '-q'], workspaceRoot);
    } catch (err) {
        stream.markdown(`Falha ao instalar dependências: ${err}\n\nVerifique se o Python está acessível em \`${python}\`.`);
        return;
    }

    // 2. Subir o servidor
    stream.markdown('**[2/2]** Iniciando servidor…');

    serverProcess = cp.spawn(
        python,
        ['-m', 'uvicorn', 'main_api:app', '--port', String(SERVER_PORT)],
        { cwd: workspaceRoot }
    );

    serverProcess.on('error', (err) => {
        vscode.window.showErrorMessage(`DE Agent: falha ao iniciar servidor — ${err.message}`);
        serverProcess = null;
    });

    serverProcess.on('exit', () => { serverProcess = null; });

    const ready = await waitForServer();

    if (ready) {
        stream.markdown(
            'Tudo pronto! Pode fazer sua pergunta.\n\n' +
            '`/reset` limpa o contexto · `/stop` encerra o servidor'
        );
    } else {
        stream.markdown('Timeout ao aguardar o servidor. Veja os logs no terminal para mais detalhes.');
        serverProcess?.kill();
    }
}

function stopServer(stream: vscode.ChatResponseStream): void {
    if (!serverProcess) {
        stream.markdown('Servidor não está em execução.');
        return;
    }
    serverProcess.kill();
    serverProcess = null;
    stream.markdown('Servidor encerrado.');
}

// ---------------------------------------------------------------------------
// Handler principal do chat participant
// ---------------------------------------------------------------------------

async function handleRequest(
    request: vscode.ChatRequest,
    _ctx: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    _token: vscode.CancellationToken
): Promise<void> {
    switch (request.command) {
        case 'start': return startServer(stream);
        case 'stop':  return stopServer(stream);
        case 'reset':
            try {
                await fetch(`${API_BASE}/reset`, { method: 'POST' });
                stream.markdown('Contexto do agente limpo.');
            } catch {
                stream.markdown(offlineMessage());
            }
            return;
    }

    if (!request.prompt.trim()) {
        stream.markdown('Digite uma mensagem para o agente, ou use `/start` para iniciar o servidor.');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: request.prompt }),
        });

        if (!res.ok) {
            stream.markdown(`Erro do servidor: HTTP ${res.status}.`);
            return;
        }

        const data = (await res.json()) as { response: string };
        stream.markdown(data.response);
    } catch {
        stream.markdown(offlineMessage());
    }
}

function offlineMessage(): string {
    return (
        '> **Servidor do agente offline.**\n\n' +
        'Use o comando `/start` para iniciá-lo:\n' +
        '```\n@de-agent /start\n```'
    );
}

// ---------------------------------------------------------------------------
// Ativação / desativação da extensão
// ---------------------------------------------------------------------------

export function activate(context: vscode.ExtensionContext): void {
    const participant = vscode.chat.createChatParticipant(PARTICIPANT_ID, handleRequest);
    participant.iconPath = new vscode.ThemeIcon('circuit-board');
    context.subscriptions.push(participant);
}

export function deactivate(): void {
    serverProcess?.kill();
}

