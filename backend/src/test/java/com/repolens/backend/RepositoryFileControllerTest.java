package com.repolens.backend;

import com.repolens.backend.controller.RepositoryFileController;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.repository.RepositoryFileRepository;
import com.repolens.backend.service.RepositoryFileService;
import com.repolens.backend.service.RepositoryService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class RepositoryFileControllerTest {

    @Test
    void shouldGetRepositoryFiles() {
        RepositoryService repositoryService = mock(RepositoryService.class);
        RepositoryFileRepository fileRepository = mock(RepositoryFileRepository.class);

        RepositoryFileService service =
                new RepositoryFileService(repositoryService, fileRepository);

        RepositoryFile file1 =
                new RepositoryFile("Repository.java", "Java", "src/Repository.java");
        RepositoryFile file2 =
                new RepositoryFile("Service.java", "Java", "src/Service.java");
        RepositoryFile file3 =
                new RepositoryFile("README.md", "Markdown", "README.md");

        when(repositoryService.getRepository(1L))
                .thenReturn(new com.repolens.backend.model.Repository(
                        "RepoLens",
                        "https://github.com/example/RepoLens"
                ));

        when(fileRepository.findByRepositoryId(1L))
                .thenReturn(List.of(file1, file2, file3));

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
        RepositoryService repositoryService = mock(RepositoryService.class);
        RepositoryFileRepository fileRepository = mock(RepositoryFileRepository.class);

        RepositoryFileService service =
                new RepositoryFileService(repositoryService, fileRepository);

        when(repositoryService.getRepository(0L))
                .thenThrow(new IllegalArgumentException("Repository not found: 0"));

        RepositoryFileController controller =
                new RepositoryFileController(service);

        assertThrows(
                IllegalArgumentException.class,
                () -> controller.getFiles(0L)
        );
    }
}