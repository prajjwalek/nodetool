import { create } from "zustand";
import { client } from "./ApiClient";
import { CachedModel, FunctionModel, LlamaModel } from "./ApiTypes";
import { QueryClient } from "@tanstack/react-query";

type ModelStore = {
  queryClient: QueryClient | null;
  setQueryClient(queryClient: QueryClient): unknown;
  modelFiles: Record<string, string[]>;
  functionModels: FunctionModel[];
  llamaModels: LlamaModel[];
  invalidate: () => void;
  huggingFaceModels: CachedModel[];
  loadFunctionModels: () => Promise<FunctionModel[]>;
  loadLlamaModels: () => Promise<LlamaModel[]>;
  loadHuggingFaceModels: () => Promise<CachedModel[]>;
  loadFiles: (folder: string) => Promise<string[]>;
};

const useModelStore = create<ModelStore>((set, get) => ({
  queryClient: null,
  modelFiles: {},
  functionModels: [],
  llamaModels: [],
  huggingFaceModels: [],
  setQueryClient: (queryClient: QueryClient) => {
    set({ queryClient });
  },
  invalidate: () => {
    get().queryClient?.invalidateQueries();
  },
  loadHuggingFaceModels: async () => {
    const { error, data } = await client.GET("/api/models/huggingface_models", {});
    if (error) {
      throw new Error("Failed to fetch models: " + error);
    }
    set({
      huggingFaceModels: data
    });
    return data;
  },
  loadLlamaModels: async () => {
    const { error, data } = await client.GET("/api/models/llama_models", {});
    if (error) {
      throw new Error("Failed to fetch models: " + error);
    }
    set({
      llamaModels: data
    });
    return data;
  },
  loadFunctionModels: async () => {
    const { error, data } = await client.GET("/api/models/function_models", {});
    if (error) {
      throw new Error("Failed to fetch models: " + error);
    }
    set({
      functionModels: data
    });
    return data;
  },
  loadFiles: async (folder: string) => {
    const { error, data } = await client.GET("/api/models/{folder}", {
      params: { path: { folder } }
    });
    const modelFiles = get().modelFiles;
    if (error) {
      throw new Error("Failed to fetch models: " + error);
    }
    set({
      modelFiles: {
        ...modelFiles,
        [folder]: data
      }
    });
    return data;
  }
}));

export default useModelStore;
