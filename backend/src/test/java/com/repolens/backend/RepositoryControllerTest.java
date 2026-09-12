package com.repolens.backend;

import com.repolens.backend.controller.RepositoryController;
import com.repolens.backend.model.Repository;
import com.repolens.backend.repository.RepositoryJpaRepository;
import com.repolens.backend.service.RepositoryService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class RepositoryControllerTest {

    @Test
    void shouldReturnRepositoryWhenIdExists() {
        RepositoryJpaRepository repositoryJpaRepository =
                mock(RepositoryJpaRepository.class);

        Repository repository = new Repository();

        repository.setId(1L);
        repository.setName("RepoLens");
        repository.setUrl(
                "https://github.com/PawaniB13/RepoLens"
        );

        when(repositoryJpaRepository.findAll())
                .thenReturn(List.of(repository));

        RepositoryService repositoryService =
                new RepositoryService(repositoryJpaRepository);

        RepositoryController controller =
                new RepositoryController(repositoryService);

        ResponseEntity<Repository> response =
                controller.getRepository(1L);

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals(1L, response.getBody().getId());
        assertEquals("RepoLens", response.getBody().getName());
    }

    @Test
    void shouldReturnNotFoundWhenRepositoryDoesNotExist() {
        RepositoryJpaRepository repositoryJpaRepository =
                mock(RepositoryJpaRepository.class);

        when(repositoryJpaRepository.findAll())
                .thenReturn(List.of());

        RepositoryService repositoryService =
                new RepositoryService(repositoryJpaRepository);

        RepositoryController controller =
                new RepositoryController(repositoryService);

        ResponseEntity<Repository> response =
                controller.getRepository(999L);

        assertEquals(404, response.getStatusCode().value());
        assertNull(response.getBody());
    }
}