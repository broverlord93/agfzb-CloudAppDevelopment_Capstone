const Cloudant = require('@cloudant/cloudant');

async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    const db = cloudant.use('dealerships');

    const selector = {
            "selector": {
            }
        }

    let atLeastOneParamProvided = false;

    if (params.state){
        selector.selector["state"] = { "$eq": params.state };
        atLeastOneParamProvided = true;
    }
    if (params.dealerId){
        selector.selector["id"] = { "$eq": parseInt(params.dealerId) };
        atLeastOneParamProvided = true;
    }

    try{
        if (atLeastOneParamProvided){
            const response = await db.find(selector);
            return {
                "statusCode": response.docs.length === 0 ? 404 : 200,
                "headers": { "Content-Type": "application/json" },
                "body": response.docs
            };
        } else {
            const response = await db.list({ "include_docs": true });
            return {
                "statusCode": 200,
                "headers": { "Content-Type": "application/json" },
                "body": response.rows
            };
        }
    } catch (error){
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": error.message
        };
    }
}
