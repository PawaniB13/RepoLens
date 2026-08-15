package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryStatistics;
import org.springframework.stereotype.Service;

@Service
public class RepositoryStatisticsService {

    public RepositoryStatistics getStatistics(Long repositoryId) {

        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException("Repository ID must be positive");
        }

        return new RepositoryStatistics(
                repositoryId,
                "RepoLens",
                10,
                5,
                3,
                2
        );
    }
}