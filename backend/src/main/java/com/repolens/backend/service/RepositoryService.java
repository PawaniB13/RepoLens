package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.repository.RepositoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryService {

    private final RepositoryRepository repositoryRepository;

    public RepositoryService(RepositoryRepository repositoryRepository) {
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
        return repositoryRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found: " + id
                        )
                );
    }

    public Repository importRepository(String name, String url) {
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
}