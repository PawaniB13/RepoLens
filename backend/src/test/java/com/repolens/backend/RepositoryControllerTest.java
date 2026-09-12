package com.repolens.backend;

import com.repolens.backend.controller.RepositoryController;
import com.repolens.backend.repository.RepositoryRepository;
import com.repolens.backend.service.GitHubService;
import com.repolens.backend.service.RepositoryService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;

class RepositoryControllerTest {

    @Test
    void controllerCanBeCreated() {
        RepositoryRepository repositoryRepository =
                mock(RepositoryRepository.class);

        RepositoryService repositoryService =
                new RepositoryService(repositoryRepository);

        GitHubService gitHubService =
                new GitHubService(repositoryService);

        RepositoryController controller =
                new RepositoryController(
                        repositoryService,
                        gitHubService
                );

        assertNotNull(controller);
    }
}