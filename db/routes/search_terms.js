const { GoogleSpreadsheet } = require('google-spreadsheet');

const { sheetId, apiKey } = require('../config').google;

const doc = new GoogleSpreadsheet(sheetId);
doc.useApiKey(apiKey);

const typeIndexes = {
    'political': 0,
    'other': 1
};

module.exports = app => {
    // TODO: Pass political ideology as number so that we don't have to get full sheet contents
    app.get('/search_terms/:type/:category', async function(req, res, next) {
        /**
         * Fetches all search terms from Google Sheet
         * @param params.type       - Type of terms to fetch. 
         *      Possible values: political, other
         * @param params.category   - Integer representing category.
         *      Refers to column in Google Sheet
         */
        const { type, category } = req.params;
        const index = typeIndexes[type];

        if (isNaN(index)) {
            return res.status(400).send('Invalid type given');
        }

        try {
            await doc.loadInfo();
            const rows = await doc.sheetsByIndex[index].getRows();

            const terms = [];
            rows.forEach(row => {
                const val = row._rawData[category];
                if (val !== '' && val !== undefined && val !== null) {
                    terms.push(val);
                }
            });

            if (terms.length == 0) {
                return res.status(404).send('No search terms found');
            }

            res.send(terms);
        } catch (err) {
            next(err);
        }
    });
}