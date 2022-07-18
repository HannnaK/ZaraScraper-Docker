DROP TABLE IF EXISTS "categories";

CREATE TABLE "categories"
(
    "category" TEXT    NOT NULL,
    "link" TEXT    NOT NULL,
    "is_on_sale" BOOLEAN NOT NULL CHECK ("is_on_sale" IN (0, 1))
);
INSERT INTO "categories"
VALUES ('od 70%', 'https://www.zara.com/pl/pl/man-from-70-l5430.html?v1=2112329', 1),
('zara athleticz', 'https://www.zara.com/pl/pl/zara-athleticz-collection-l4712.html?v1=2110962', 1),
('garnitury', 'https://www.zara.com/pl/pl/mezczyzna-garnitury-l808.html?v1=2110780', 1),
('koszule', 'https://www.zara.com/pl/pl/mezczyzna-koszule-l737.html?v1=2109801', 1),
('koszulki | koszulki polo', 'https://www.zara.com/pl/pl/man-tshirts-polos-l5450.html?v1=2109819', 1),
('spodnie', 'https://www.zara.com/pl/pl/mezczyzna-spodnie-l838.html?v1=2110975', 1),
('jeansy', 'https://www.zara.com/pl/pl/mezczyzna-jeansy-l659.html?v1=2110815', 1),
('spodenki', 'https://www.zara.com/pl/pl/mezczyzna-bermudy-l592.html?v1=2110810', 1),
('bluzy', 'https://www.zara.com/pl/pl/mezczyzna-bluzy-l821.html?v1=2110970', 1),
('swetry', 'https://www.zara.com/pl/pl/mezczyzna-na-drutach-l681.html?v1=2109795', 1),
('kurtki', 'https://www.zara.com/pl/pl/mezczyzna-kurtki-l640.html?v1=2110795', 1),
('kurtki koszulowe', 'https://www.zara.com/pl/pl/man-overshirts-l3174.html?v1=2111376', 1),
('kamizelki', 'https://www.zara.com/pl/pl/mezczyzna-kurtki-kamizelki-l1650.html?v1=2110779', 1),
('plaszcze | marynarki', 'https://www.zara.com/pl/pl/man-blazer-coats-l5460.html?v1=2109818', 1),
('buty', 'https://www.zara.com/pl/pl/mezczyzna-buty-l769.html?v1=2110821', 1),
('torby | plecaki', 'https://www.zara.com/pl/pl/mezczyzna-torby-l563.html?v1=2111832', 1),
('akcesoria', 'https://www.zara.com/pl/pl/mezczyzna-akcesoria-l537.html?v1=2110983', 1),
('perfumy', 'https://www.zara.com/pl/pl/mezczyzna-akcesoria-perfumy-l551.html?v1=2110794', 1),


('nowosci', 'https://www.zara.com/pl/pl/mezczyzna-nowosci-l711.html', 0),
('zara athleticz', 'https://www.zara.com/pl/pl/zara-athleticz-collection-l4712.html?v1=2112945', 0),
('kolekcja basic', 'https://www.zara.com/pl/pl/mezczyzna-basics-l587.html?v1=2112966', 0),
('garnitury', 'https://www.zara.com/pl/pl/mezczyzna-garnitury-l808.html?v1=2113078', 0),
('koszule', 'https://www.zara.com/pl/pl/mezczyzna-koszule-l737.html?v1=2113199', 0),
('t-shirty', 'https://www.zara.com/pl/pl/mezczyzna-t-shirty-l855.html?v1=2113240', 0),
('koszulki polo', 'https://www.zara.com/pl/pl/mezczyzna-koszulki-polo-l733.html?v1=2113259', 0),
('spodnie', 'https://www.zara.com/pl/pl/mezczyzna-spodnie-l838.html?v1=2113288', 0),
('jeansy', 'https://www.zara.com/pl/pl/mezczyzna-jeansy-l659.html?v1=2119348', 0),
('spodenki', 'https://www.zara.com/pl/pl/mezczyzna-bermudy-l592.html?v1=2113319', 0),
('kurtki', 'https://www.zara.com/pl/pl/mezczyzna-kurtki-l640.html?v1=2113031', 0),
('bluzy', 'https://www.zara.com/pl/pl/mezczyzna-bluzy-l821.html?v1=2113165', 0),
('swetry', 'https://www.zara.com/pl/pl/mezczyzna-na-drutach-l681.html?v1=2113125', 0),
('kurtki koszulowe', 'https://www.zara.com/pl/pl/man-overshirts-l3174.html?v1=2113048', 0),
('marynarki', 'https://www.zara.com/pl/pl/mezczyzna-blazers-l608.html?v1=2113099', 0),
('dresy', 'https://www.zara.com/pl/pl/mezczyzna-jogging-l679.html?v1=2113135', 0),
('buty', 'https://www.zara.com/pl/pl/mezczyzna-buty-l769.html?v1=2119401', 0),
('torby | plecaki', 'https://www.zara.com/pl/pl/mezczyzna-torby-l563.html?v1=2119450', 0),
('stroje kapielowe', 'https://www.zara.com/pl/pl/mezczyzna-beachwear-l590.html?v1=2119501', 0),
('akcesoria', 'https://www.zara.com/pl/pl/mezczyzna-akcesoria-l537.html?v1=2119495', 0),
('perfumy', 'https://www.zara.com/pl/pl/mezczyzna-akcesoria-perfumy-l551.html?v1=2119507', 0);
