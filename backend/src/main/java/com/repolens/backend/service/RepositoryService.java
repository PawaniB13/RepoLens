package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.repository.RepositoryJpaRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryService {

    private final RepositoryJpaRepository repositoryJpaRepository;

    public RepositoryService(RepositoryJpaRepository repositoryJpaRepository) {
        this.repositoryJpaRepository = repositoryJpaRepository;
    }

    public RepositoryService() {
        this.repositoryJpaRepository = null;
    }

    public List<Repository> getRepositories() {
    if (repositoryJpaRepository == null) {
        return List.of(
                new Repository(
                        1L,
                        "RepoLens",
                        "https://github.com/PawaniB13/RepoLens"
                )
        );
    }

    return repositoryJpaRepository.findAll();
}

    public Repository saveRepository(Repository repository) {
        if (repositoryJpaRepository == null) {
            return repository;
        }

        return repositoryJpaRepository.save(repository);
    }

    public List<Repository> searchRepositories(String query) {
        if (query == null || query.isBlank()) {
            return List.of();
        }

        String normalizedQuery = query.trim().toLowerCase();

        return getRepositories().stream()
                .filter(repository ->
                        repository.getName() != null
                                && repository.getName()
                                .toLowerCase()
                                .contains(normalizedQuery))
                .toList();
    }
}