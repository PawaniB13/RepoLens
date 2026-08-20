package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryAnalysis;
import org.springframework.stereotype.Service;

@Service
public class RepositoryAnalysisService {

    public RepositoryAnalysis analyzeRepository(Long repositoryId) {

    if (repositoryId == null || repositoryId <= 0) {
        throw new IllegalArgumentException("Repository ID must be positive");
    }

    return new RepositoryAnalysis(
            repositoryId,
            "RepoLens",
            10,
            5,
            3
    );
}
}