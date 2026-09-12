import { mockAnalysis } from "./mockdata";

export const getLatestAnalysis = async (repositoryId) => {
  if (repositoryId !== mockAnalysis.repositoryId) {
    return null;
  }

  return mockAnalysis;
};