package com.repolens.backend;

import com.repolens.backend.controller.RepositoryStatisticsController;
import com.repolens.backend.model.RepositoryStatistics;
import com.repolens.backend.service.RepositoryFileService;
import com.repolens.backend.service.RepositoryStatisticsService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryStatisticsControllerTest {

    @Test
    void shouldGetRepositoryStatistics() {
        RepositoryFileService fileService = new RepositoryFileService();
        RepositoryStatisticsService service =
                new RepositoryStatisticsService(fileService);

        RepositoryStatisticsController controller =
                new RepositoryStatisticsController(service);

        ResponseEntity<RepositoryStatistics> response =
                controller.getStatistics(1L);

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals(1L, response.getBody().getRepositoryId());
        assertEquals("RepoLens", response.getBody().getRepositoryName());
        assertEquals(3, response.getBody().getTotalFiles());
        assertEquals(3, response.getBody().getJavaFiles());
        assertEquals(0, response.getBody().getJavascriptFiles());
        assertEquals(0, response.getBody().getOtherFiles());
    }

    @Test
    void shouldRejectInvalidRepositoryId() {
        RepositoryFileService fileService = new RepositoryFileService();
        RepositoryStatisticsService service =
                new RepositoryStatisticsService(fileService);

        RepositoryStatisticsController controller =
                new RepositoryStatisticsController(service);

        assertThrows(
                IllegalArgumentException.class,
                () -> controller.getStatistics(0L)
        );
    }
}