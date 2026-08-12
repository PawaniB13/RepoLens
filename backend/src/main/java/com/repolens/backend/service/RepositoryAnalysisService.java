package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryAnalysis;
import org.springframework.stereotype.Service;

@Service
public class RepositoryAnalysisService {

    public RepositoryAnalysis analyzeRepository(Long repositoryId) {

        return new RepositoryAnalysis(
                repositoryId,
                "RepoLens",
                10,
                5,
                3
        );
    }
}