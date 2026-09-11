package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryService {

    public List<Repository> getRepositories() {
        return List.of(
                new Repository(
                        1L,
                        "RepoLens",
                        "https://github.com/PawaniB13/RepoLens"
                )
        );
    }

    public List<Repository> searchRepositories(String query) {
        if (query == null || query.isBlank()) {
            return List.of();
        }

        String normalizedQuery = query.trim().toLowerCase();

        return getRepositories().stream()
                .filter(repository ->
                        repository.getName()
                                .toLowerCase()
                                .contains(normalizedQuery))
                .toList();
    }
}

