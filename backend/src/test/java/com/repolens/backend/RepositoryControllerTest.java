package com.repolens.backend;

import com.repolens.backend.controller.RepositoryController;
import com.repolens.backend.model.Repository;
import com.repolens.backend.service.RepositoryService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryControllerTest {

    @Test
    void shouldReturnRepositoryWhenIdExists() {
        RepositoryService service = new RepositoryService();
        RepositoryController controller = new RepositoryController(service);

        ResponseEntity<Repository> response = controller.getRepository(1L);

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals(1L, response.getBody().getId());
        assertEquals("RepoLens", response.getBody().getName());
    }

    @Test
    void shouldReturnNotFoundWhenRepositoryDoesNotExist() {
        RepositoryService service = new RepositoryService();
        RepositoryController controller = new RepositoryController(service);

        ResponseEntity<Repository> response = controller.getRepository(999L);

        assertEquals(404, response.getStatusCode().value());
        assertNull(response.getBody());
    }
}