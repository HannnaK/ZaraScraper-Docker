DROP TABLE IF EXISTS "clothes_details";

CREATE TABLE "clothes_details"
(
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "category" TEXT    NOT NULL,
    "index" TEXT    NOT NULL,
    "link" TEXT    NOT NULL,
    "is_on_sale" TEXT    NOT NULL,
    "name" TEXT,
    "price" REAL    NOT NULL,
    "old_price" TEXT,
    "description" TEXT,
    "colors" TEXT,
    "sizes" TEXT
);
