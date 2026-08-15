package com.repolens.backend;

import com.repolens.backend.controller.RepositoryStatisticsController;
import com.repolens.backend.model.RepositoryStatistics;
import com.repolens.backend.service.RepositoryStatisticsService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryStatisticsControllerTest {

    @Test
    void shouldGetRepositoryStatistics() {
        RepositoryStatisticsService service = new RepositoryStatisticsService();
        RepositoryStatisticsController controller =
                new RepositoryStatisticsController(service);

        ResponseEntity<RepositoryStatistics> response =
                controller.getStatistics(1L);

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals(1L, response.getBody().getRepositoryId());
        assertEquals("RepoLens", response.getBody().getRepositoryName());
        assertEquals(10, response.getBody().getTotalFiles());
        assertEquals(5, response.getBody().getJavaFiles());
        assertEquals(3, response.getBody().getJavascriptFiles());
        assertEquals(2, response.getBody().getOtherFiles());
    }

    @Test
    void shouldRejectInvalidRepositoryId() {
        RepositoryStatisticsService service = new RepositoryStatisticsService();
        RepositoryStatisticsController controller =
                new RepositoryStatisticsController(service);

        assertThrows(
                IllegalArgumentException.class,
                () -> controller.getStatistics(0L)
        );
    }
}
