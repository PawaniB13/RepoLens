package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RepositoryService {

    private final List<Repository> repositories = new ArrayList<>();

    public RepositoryService() {
        repositories.add(
                new Repository(
                        1L,
                        "RepoLens",
                        "https://github.com/PawaniB13/RepoLens"
                )
        );
    }

    public List<Repository> getRepositories() {
        return repositories;
    }

    public List<Repository> searchRepositories(String query) {
        if (query == null || query.isBlank()) {
            return List.of();
        }

        String normalizedQuery = query.trim().toLowerCase();

        return repositories.stream()
                .filter(repository ->
                        repository.getName()
                                .toLowerCase()
                                .contains(normalizedQuery))
                .toList();
    }

    public Repository importRepository(String name, String url) {
        Long nextId = repositories.stream()
                .mapToLong(repository -> repository.getId())
                .max()
                .orElse(0L) + 1;

        Repository repository = new Repository(nextId, name, url);
        repositories.add(repository);

        return repository;
    }
}