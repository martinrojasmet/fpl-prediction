-- AlterTable
CREATE SEQUENCE double_gw_id_seq;
ALTER TABLE "double_gw" ALTER COLUMN "id" SET DEFAULT nextval('double_gw_id_seq');
ALTER SEQUENCE double_gw_id_seq OWNED BY "double_gw"."id";

-- AlterTable
CREATE SEQUENCE fixtures_id_seq;
ALTER TABLE "fixtures" ALTER COLUMN "id" SET DEFAULT nextval('fixtures_id_seq');
ALTER SEQUENCE fixtures_id_seq OWNED BY "fixtures"."id";

-- AlterTable
CREATE SEQUENCE games_id_seq;
ALTER TABLE "games" ALTER COLUMN "id" SET DEFAULT nextval('games_id_seq');
ALTER SEQUENCE games_id_seq OWNED BY "games"."id";

-- AlterTable
ALTER TABLE "players" ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "players_pkey" PRIMARY KEY ("id");

-- AlterTable
CREATE SEQUENCE predictions_id_seq;
ALTER TABLE "predictions" ALTER COLUMN "id" SET DEFAULT nextval('predictions_id_seq');
ALTER SEQUENCE predictions_id_seq OWNED BY "predictions"."id";

-- AlterTable
ALTER TABLE "teams" ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "teams_pkey" PRIMARY KEY ("id");
