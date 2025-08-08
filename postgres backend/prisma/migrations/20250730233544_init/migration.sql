-- CreateTable
CREATE TABLE "fixtures" (
    "id" INTEGER NOT NULL,
    "season" TEXT NOT NULL,
    "gw" INTEGER NOT NULL,
    "fpl_element" INTEGER NOT NULL,
    "local_understat_id" DOUBLE PRECISION,
    "local_understat_fixture" DOUBLE PRECISION,
    "fpl_name" TEXT NOT NULL,
    "understat_name" TEXT NOT NULL,
    "position" INTEGER NOT NULL,
    "fpl_team" INTEGER NOT NULL,
    "understat_team" TEXT NOT NULL,
    "opponent_fpl_team_number" INTEGER NOT NULL,
    "fpl_kickoff_time" TIMESTAMP(3) NOT NULL,
    "understat_date" TIMESTAMP(3) NOT NULL,
    "value" INTEGER NOT NULL,
    "points" INTEGER NOT NULL,
    "minutes" INTEGER NOT NULL,
    "goals_scored" INTEGER NOT NULL,
    "xG" DOUBLE PRECISION NOT NULL,
    "goals_conceded" INTEGER NOT NULL,
    "assists" INTEGER NOT NULL,
    "xA" DOUBLE PRECISION NOT NULL,
    "yellow_cards" INTEGER NOT NULL,
    "red_cards" INTEGER NOT NULL,
    "clean_sheets" INTEGER NOT NULL,
    "key_passes" DOUBLE PRECISION NOT NULL,
    "own_goals" INTEGER NOT NULL,
    "penalties_missed" INTEGER NOT NULL,
    "penalties_saved" INTEGER NOT NULL,
    "saves" INTEGER NOT NULL,
    "bonus" INTEGER NOT NULL,
    "team_a_score" INTEGER NOT NULL,
    "team_h_score" INTEGER NOT NULL,
    "was_home" BOOLEAN NOT NULL,
    "expected_assists" DOUBLE PRECISION,
    "expected_goals" DOUBLE PRECISION,

    CONSTRAINT "fixtures_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "players" (
    "fpl_name" TEXT NOT NULL,
    "understat_name" TEXT,
    "fpl_202425" DOUBLE PRECISION NOT NULL,
    "opta_id" INTEGER
);

-- CreateTable
CREATE TABLE "teams" (
    "season" TEXT NOT NULL,
    "team" INTEGER NOT NULL,
    "team_name" TEXT NOT NULL,
    "definite_team_number" INTEGER NOT NULL,
    "understat_name" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "predictions" (
    "id" INTEGER NOT NULL,
    "understat_name" TEXT NOT NULL,
    "opta_id" INTEGER NOT NULL,
    "gw" INTEGER NOT NULL,
    "opponent_team" INTEGER NOT NULL,
    "global_predicted_points" DOUBLE PRECISION NOT NULL,
    "opponent_predicted_points" DOUBLE PRECISION NOT NULL,
    "combined_predicted_points" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "predictions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "games" (
    "id" INTEGER NOT NULL,
    "understat_id" INTEGER NOT NULL,
    "date" TEXT NOT NULL,
    "home" TEXT NOT NULL,
    "gw" INTEGER NOT NULL,
    "home_goals" DOUBLE PRECISION NOT NULL,
    "home_xG" DOUBLE PRECISION NOT NULL,
    "home_assists" DOUBLE PRECISION NOT NULL,
    "home_xA" DOUBLE PRECISION NOT NULL,
    "rolling_home_goals" DOUBLE PRECISION NOT NULL,
    "rolling_home_xG" DOUBLE PRECISION NOT NULL,
    "rolling_home_assists" DOUBLE PRECISION NOT NULL,
    "rolling_home_xA" DOUBLE PRECISION NOT NULL,
    "home_team_code" INTEGER NOT NULL,
    "away" TEXT NOT NULL,
    "away_goals" DOUBLE PRECISION NOT NULL,
    "away_xG" DOUBLE PRECISION NOT NULL,
    "away_assists" DOUBLE PRECISION NOT NULL,
    "away_xA" DOUBLE PRECISION NOT NULL,
    "rolling_away_goals" DOUBLE PRECISION NOT NULL,
    "rolling_away_xG" DOUBLE PRECISION NOT NULL,
    "rolling_away_assists" DOUBLE PRECISION NOT NULL,
    "rolling_away_xA" DOUBLE PRECISION NOT NULL,
    "away_team_code" INTEGER NOT NULL,
    "result" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "games_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "double_gw" (
    "id" INTEGER NOT NULL,
    "home" TEXT NOT NULL,
    "away" TEXT NOT NULL,
    "gw" INTEGER NOT NULL,
    "original_gw" INTEGER NOT NULL,
    "understat_id" INTEGER NOT NULL,
    "season" TEXT NOT NULL,

    CONSTRAINT "double_gw_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "players_fpl_name_key" ON "players"("fpl_name");

-- CreateIndex
CREATE UNIQUE INDEX "teams_definite_team_number_key" ON "teams"("definite_team_number");
