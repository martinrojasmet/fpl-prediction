import express from 'express';

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

app.get('/', (req, res) => {
    res.status(200).send('Hello World!');
}
);

app.listen(3000, async () => {
    console.log('Server is running on http://localhost:3000');
});
