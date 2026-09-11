package com.repolens.backend.repository;

import com.repolens.backend.model.Repository;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RepositoryJpaRepository extends JpaRepository<Repository, Long> {
}