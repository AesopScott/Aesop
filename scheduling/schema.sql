-- Run this once to create the tables needed by the scheduler.

CREATE TABLE IF NOT EXISTS oauth_tokens (
  id            INT          NOT NULL DEFAULT 1,
  access_token  TEXT         NOT NULL,
  refresh_token TEXT         NOT NULL,
  expires_at    INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS bookings (
  id               INT UNSIGNED  NOT NULL AUTO_INCREMENT,
  outlook_event_id VARCHAR(512)  NOT NULL,
  guest_name       VARCHAR(255)  NOT NULL,
  guest_email      VARCHAR(255)  NOT NULL,
  start_time       DATETIME      NOT NULL,
  end_time         DATETIME      NOT NULL,
  created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX idx_start (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
