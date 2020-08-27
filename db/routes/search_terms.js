const { GoogleSpreadsheet } = require('google-spreadsheet');

const { sheetId, apiKey } = require('../config').google;

const doc = new GoogleSpreadsheet(sheetId);
doc.useApiKey(apiKey);

module.exports = app => {
    // TODO: Pass political ideology as number so that we don't have to get full sheet contents
    app.get('/search_terms', async function(req, res, next) {
        /**
         * Fetches all search terms from Google Sheet
         */
        try {
            await doc.loadInfo();
            const rows = await doc.sheetsByIndex[0].getRows()

            const terms = [];
            rows.forEach(row => {
                row._rawData.forEach((cell, j) => {
                    if (j == terms.length) terms.push([]);
                    if (cell === '') return;
                    terms[j].push(cell);
                });
            });

            res.send(terms)
        } catch (err) {
            next(err);
        }
    });
}