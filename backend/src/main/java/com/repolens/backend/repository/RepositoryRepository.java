package com.repolens.backend.repository;

import com.repolens.backend.model.Repository;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface RepositoryRepository
        extends JpaRepository<Repository, Long> {

    List<Repository> findByNameContainingIgnoreCase(String name);

    Optional<Repository> findByUrl(String url);
}