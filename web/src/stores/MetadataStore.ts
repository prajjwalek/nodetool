import { create } from "zustand";
import { NodeMetadata } from "./ApiTypes";

type MetadataStore = {
  metadata: Record<string, NodeMetadata>;
  setMetadata: (metadata: Record<string, NodeMetadata>) => void;
  getMetadata: (nodeType: string) => NodeMetadata | undefined;
};
const useMetadataStore = create<MetadataStore>((set, get) => ({
  metadata: {},
  setMetadata: (metadata) => set({ metadata }),
  getMetadata: (nodeType) => {
    return get().metadata[nodeType];
  }
}));

export default useMetadataStore;
