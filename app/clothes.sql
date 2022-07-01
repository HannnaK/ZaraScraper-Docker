DROP TABLE IF EXISTS "clothes";

CREATE TABLE "clothes"
(
    "category" TEXT    NOT NULL,
    "clothes" TEXT    NOT NULL,
    "is_on_sale" BOOLEAN NOT NULL CHECK ("is_on_sale" IN (0, 1))
);