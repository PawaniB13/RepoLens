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
                        "https://github.com/example/repolens-backend"
                )
        );
    }

    public List<Repository> getRepositories() {
        return repositories;
    }

    public List<Repository> searchRepositories(String query) {
        if (query == null || query.isBlank()) {
            return repositories;
        }

        String search = query.toLowerCase();

        return repositories.stream()
                .filter(repository ->
                        repository.getName().toLowerCase().contains(search)
                                || repository.getUrl().toLowerCase().contains(search)
                )
                .toList();
    }

    public Repository importRepository(String name, String url) {
        Repository repository = new Repository(
                (long) repositories.size() + 1,
                name,
                url
        );

        repositories.add(repository);
        return repository;
    }
}