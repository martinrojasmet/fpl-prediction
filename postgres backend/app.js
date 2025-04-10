import express from 'express';

import fixtureRouter from './routes/fixture.route.js';
import playerRouter from './routes/player.routes.js';
import teamRouter from './routes/team.routes.js';
import gameRouter from './routes/game.routes.js';
import predictionRouter from './routes/prediction.route.js';

import errorMiddleware from './middlewares/error.middleware.js';

import { PORT } from './config/env.js';

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

app.use('/api/players', playerRouter);
app.use('/api/teams', teamRouter);
app.use('/api/fixtures', fixtureRouter);
app.use('/api/games', gameRouter);
app.use('/api/predictions', predictionRouter);

app.use(errorMiddleware)

app.listen(PORT, async () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
