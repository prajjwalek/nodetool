import { create } from 'zustand';

interface Download {
    status: 'idle' | 'running' | 'completed' | 'cancelled' | 'error' | 'start' | 'progress';
    repoId: string;
    downloadedBytes: number;
    totalBytes: number;
    totalFiles?: number;
    downloadedFiles?: number;
    currentFile?: string;
    message?: string;
}

interface HuggingFaceStore {
    downloads: Record<string, Download>;
    ws: WebSocket | null;
    connectWebSocket: () => Promise<WebSocket>;
    disconnectWebSocket: () => void;
    addDownload: (repoId: string) => void;
    updateDownload: (repoId: string, update: Partial<Download>) => void;
    removeDownload: (repoId: string) => void;
    startDownload: (repoId: string) => void;
    cancelDownload: (repoId: string) => void;
}

export const useHuggingFaceStore = create<HuggingFaceStore>((set, get) => ({
    downloads: {},
    ws: null,

    connectWebSocket: async () => {
        let ws = get().ws;
        if (ws?.readyState === WebSocket.OPEN) {
            return ws;
        }

        ws = new WebSocket('ws://localhost:8000/hf/download');

        await new Promise((resolve, reject) => {
            ws.onopen = resolve;
            ws.onerror = reject;
        });

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('ws message', data);
            if (data.repo_id) {
                get().updateDownload(data.repo_id, {
                    status: data.status,
                    repoId: data.repo_id,
                    downloadedBytes: data.downloaded_bytes,
                    totalBytes: data.total_bytes,
                    totalFiles: data.total_files,
                    downloadedFiles: data.downloaded_files,
                    currentFile: data.current_file,
                    message: data.message,
                });
            }
        };

        set({ ws });
        return ws;
    },

    disconnectWebSocket: () => {
        const { ws } = get();
        if (ws) {
            ws.close();
            set({ ws: null });
        }
    },

    addDownload: (repoId) => set((state) => ({
        downloads: {
            ...state.downloads,
            [repoId]: {
                status: 'idle',
                repoId,
                downloadedBytes: 0,
                totalBytes: 0
            }
        },
    })),

    updateDownload: (repoId, update) => set((state) => ({
        downloads: {
            ...state.downloads,
            [repoId]: {
                ...state.downloads[repoId],
                ...update,
            },
        },
    })),

    removeDownload: (repoId) => set((state) => {
        const { [repoId]: _, ...rest } = state.downloads;
        return { downloads: rest };
    }),

    startDownload: async (repoId) => {
        const ws = await get().connectWebSocket();
        ws.send(JSON.stringify({ command: 'start_download', repo_id: repoId }));
        get().addDownload(repoId);
    },

    cancelDownload: async (repoId) => {
        const ws = await get().connectWebSocket();
        ws.send(JSON.stringify({ command: 'cancel_download', repo_id: repoId }));
    },
}));