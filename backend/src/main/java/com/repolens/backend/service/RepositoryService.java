package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.repository.RepositoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryService {

    private final RepositoryRepository repositoryRepository;

    public RepositoryService(
            RepositoryRepository repositoryRepository
    ) {
        this.repositoryRepository = repositoryRepository;
    }

    public List<Repository> getRepositories() {
        return repositoryRepository.findAll();
    }

    public List<Repository> searchRepositories(String query) {
        if (query == null || query.isBlank()) {
            return repositoryRepository.findAll();
        }

        return repositoryRepository
                .findByNameContainingIgnoreCase(query);
    }

    public Repository getRepository(Long id) {
        if (id == null || id <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        return repositoryRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found: " + id
                        )
                );
    }

    public Repository importRepository(
            String name,
            String url
    ) {
        String normalizedUrl = url.trim().toLowerCase();

        return repositoryRepository.findAll()
                .stream()
                .filter(repository ->
                        repository.getUrl() != null
                                && repository.getUrl()
                                .trim()
                                .toLowerCase()
                                .equals(normalizedUrl)
                )
                .findFirst()
                .orElseGet(() -> {
                    Repository repository =
                            new Repository(name, url);

                    return repositoryRepository.save(repository);
                });
    }

    public Repository saveRepository(
            Repository repository
    ) {
        return repositoryRepository.save(repository);
    }

    public void deleteRepository(Long id) {
        if (id == null || id <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        if (!repositoryRepository.existsById(id)) {
            throw new IllegalArgumentException(
                    "Repository not found: " + id
            );
        }

        repositoryRepository.deleteById(id);
    }
}