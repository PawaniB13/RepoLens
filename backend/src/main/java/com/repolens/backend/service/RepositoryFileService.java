package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryFile;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryFileService {

    public List<RepositoryFile> getFiles(Long repositoryId) {

        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException("Repository ID must be positive");
        }

        return List.of(
                new RepositoryFile(
                        "Repository.java",
                        "Java",
                        "src/main/java/com/repolens/backend/model/Repository.java"
                ),
                new RepositoryFile(
                        "RepositoryController.java",
                        "Java",
                        "src/main/java/com/repolens/backend/controller/RepositoryController.java"
                ),
                new RepositoryFile(
                        "RepositoryService.java",
                        "Java",
                        "src/main/java/com/repolens/backend/service/RepositoryService.java"
                )
        );
    }
}