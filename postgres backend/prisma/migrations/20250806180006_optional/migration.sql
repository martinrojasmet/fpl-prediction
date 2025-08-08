-- AlterTable
ALTER TABLE "fixtures" ALTER COLUMN "understat_name" DROP NOT NULL,
ALTER COLUMN "understat_team" DROP NOT NULL,
ALTER COLUMN "understat_date" DROP NOT NULL;
