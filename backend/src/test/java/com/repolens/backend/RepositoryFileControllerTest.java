package com.repolens.backend;

import com.repolens.backend.controller.RepositoryFileController;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.service.RepositoryFileService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryFileControllerTest {

    @Test
    void shouldGetRepositoryFiles() {
        RepositoryFileService service = new RepositoryFileService();
        RepositoryFileController controller =
                new RepositoryFileController(service);

        ResponseEntity<List<RepositoryFile>> response =
                controller.getFiles(1L);

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals(3, response.getBody().size());

        assertEquals("Repository.java",
                response.getBody().get(0).getFileName());
        assertEquals("Java",
                response.getBody().get(0).getFileType());
    }

    @Test
    void shouldRejectInvalidRepositoryId() {
        RepositoryFileService service = new RepositoryFileService();
        RepositoryFileController controller =
                new RepositoryFileController(service);

        assertThrows(
                IllegalArgumentException.class,
                () -> controller.getFiles(0L)
        );
    }
}