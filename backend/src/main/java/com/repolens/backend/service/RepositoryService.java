package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RepositoryService {

    public List<Repository> getRepositories() {
        return List.of(
                new Repository(
                        "RepoLens",
                        "https://github.com/PawaniB13/RepoLens"
                )
        );
    }
}