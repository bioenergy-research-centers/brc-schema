# Updating the BRC Schema

This page describes how to update the schema used on bioenergy.org to a new version.

AKA

## HOWTO: Updating bioenergy.org repo to a new schema version in 21 easy steps (and 19 sub-steps).

**Example:** Issue [#166](https://github.com/bioenergy-research-centers/bioenergy.org/issues/166) (Update to new version of BRC Schema - v0.1.8)

In a new branch (already created for issue_166) from bioenergy.org/main:

```
git fetch
git checkout issue_166
git pull
```

### Phase 1. Adding new schemas.

1. Build and run the import locally from your new branch before you make any code changes.

    a. Delete any local docker containers for the bioenergy.org PostgreSQL instance and app (I just do this via Docker Desktop). _We do this because we need a clean database to load the feeds into._

    b. In one shell, start the database docker image and build/run the server:

    ```
    docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 6432:5432 postgres
    docker-compose up --build
    ```

    c. When the server is up and running (you'll see `Server is running on port 8080.`), run the import code in a different shell (and save the output to a file for later). _This gives us a reference point that we can use later for contrasting records that pass/fail validation against the existing schemas._
    ```
    docker compose run api node scripts/import_datafeeds.js 2>&1 > import_datafeeds_before.txt
    ```

    d. Then shut down your instances (I just do this via Docker Desktop).

2. Locate the latest (in this case version 0.1.8) Raw JSON schema in the [brc-schema repo](https://github.com/bioenergy-research-centers/brc-schema):

    - Here is the HTML view of the latest JSON schema:
    https://github.com/bioenergy-research-centers/brc-schema/blob/main/project/jsonschema/brc_schema.schema.json
    - And this is the Raw version of that schema to be copied into your new branch:
    https://github.com/bioenergy-research-centers/brc-schema/raw/refs/heads/main/project/jsonschema/brc_schema.schema.json

3. Create a new file for this version in the `api/app/schemas` folder of your new branch:

    **Example:** `api/app/schemas/brc_schema_0.1.8.json`

4. Paste the contents of the Raw JSON schema into the new file you created.

5. Add an entry for this schema to `api/app/schemas/schema_list.json`:

    **Example:** Add this before the closing bracket in the file:
    ```
    ,{
        "version": "0.1.8",
        "filename": "brc_schema_0.1.8.json",
        "supported": false
    }
    ```

    **Note:** The `supported: false` flag is used by `api/app/models/index.js`, which adds a scope to the Dataset model that restricts queries to only those schema versions that are supported by current version of the User Interface code. This decouples schema updates from UI development by allowing BRC data feeds to update to use newer versions of the schema before the UI code supports it. This prevents UI development from blocking schema updates. Essentially, the UI developers can catch up to the latest schema whenever it is convenient (or whenever actual data is available to test with). So, in this case, since we are adding a new schema for which we don't yet have any data, we want to set the supported flag to false because we don't know if contains any breaking changes for the UI. This will enable BRCs to update their feeds to the latest schema version and allows the records to be loaded into the database without breaking the UI.

6. Determine which schema versions are in use by the current feeds.

    The 4 BRC feeds will be using older versions of the schema (pre-0.1.8 in this case) and may, in fact, each be using different versions of the schema.

    At the time of writing this (December 4, 2025):
    - JBEI uses schema_version 0.1.2
    - CABBI uses schema_version 0.1.1
    - CBI uses schema_version 0.1.4
    - GLBRC uses schema_version 0.1.7

    The feed URLs are defined in `api/app/config/datafeeds.json`, so you can check for those versions by opening each of those URLs and looking at the first line of the file, where schema_version is defined.

7. Test the new schema against all of the current feeds.

    So now we know that schema versions 0.1.1, 0.1.2, 0.1.4, and 0.1.7 are currently in use.
    But we need to validate each of these feeds against schema version 0.1.8.

    This next step is a bit janky, but this is the easiest/quickest way I've found to check for problems with the new schema.

    What we are doing is (temporarily) overwriting the contents of the the schema files currently in use:

    - `api/app/schemas/brc_schema_0.1.1.json`
    - `api/app/schemas/brc_schema_0.1.2.json`
    - `api/app/schemas/brc_schema_0.1.4.json`
    - `api/app/schemas/brc_schema_0.1.7.json`

    with the contents of the new schema:

    - `api/app/schemas/brc_schema_0.1.8.json`

    a. Copy the contents of your new schema file (`api/app/schemas/brc_schema_0.1.8.json` in this example).

    b. Paste that schema into the schema files corresponding to any schemas currently in use by the data feeds.

    **Note:** The rest of this is much like the first time we ran the export, except we're saving the import results to a different file.

    c. Delete any local docker containers for the bioenergy.org PostgreSQL instance and app (I just do this via Docker Desktop). _Again, we do this because we need a clean database to load the feeds into._

    d. In one shell, start the database docker image and build/run the server:

    ```
    docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 6432:5432 postgres
    docker-compose up --build
    ```

    e. When the server is up and running (you'll see `Server is running on port 8080.`), run the import code in a different shell (and save the output to a different filename this time):

    ```
    docker compose run api node scripts/import_datafeeds.js 2>&1 > import_datafeeds_after.txt
    ```

    This time, the import will validate each BRC against schema 0.1.8 (even though the feeds specify other versions).

    f. **Important:** After that import is completed, undo those changes to the old schema files to revert them to their original version (e.g., using `Ctrl-Z` on Windows). _We definitely don't want to commit changes to those older schema files - those changes were for running the above test only._

8. Compare the results of the earlier import to that of the new import.

    Look specifically at the pass/fail results at the bottom of these files:

    `import_datafeeds_before.txt`:
    ```
    Data Import Summary: {
      'https://bioenergy.org/JBEI/jbei.json': { valid: 265, invalid: 0 },
      'https://cabbitools.igb.illinois.edu/brc/cabbi.json': { valid: 207, invalid: 0 },
      'https://fair.ornl.gov/CBI/cbi.json': { valid: 35, invalid: 0 },
      'https://fair-data.glbrc.org/glbrc.json': { valid: 189, invalid: 24 }
    }
    ```

    `import_datafeeds_after.txt`:
    ```
    Data Import Summary: {
      'https://bioenergy.org/JBEI/jbei.json': { valid: 265, invalid: 0 },
      'https://cabbitools.igb.illinois.edu/brc/cabbi.json': { valid: 207, invalid: 0 },
      'https://fair.ornl.gov/CBI/cbi.json': { valid: 35, invalid: 0 },
      'https://fair-data.glbrc.org/glbrc.json': { valid: 191, invalid: 22 }
    }
    ```
    In these results, we see that the feeds validate at least as well with the new schema (lower set of validation results) as they do with the older schemas (upper set of validation results). If there are any expected changes in the number of records that fail validation, you can have a closer look at those records, which will be logged in these files.

9. If the goal was simply to add a new schema, and you are satisfied that feeds are importing and validating as expected, you may now commit your changes to the following files and create a PR:

    - `api/app/schemas/brc_schema_0.1.8.json`
    - `api/app/schemas/schema_list.json`

    For reference, I usually paste the contents of the before and after files as a comment to the PR so that a reviewer has something they can look at and/or replicate.

### Phase 2. User Interface updates to support new schemas.

Presuming that the PR has been merged for the schema update, the latest version of the app has been deployed to production, and there at least one data feed has switched over to using a new schema (version 0.1.8 in this example), the User Interface may now be tested to see if the new schema breaks any UI components, or if new UI fields need to be added.

10. Continuing our version 0.1.8 example, we first check out the main branch (or create a new branch from main if we will be implementing changes).

11. Enable the new schema in the User Interface.
    Remember that supported flag we set (`api/app/schemas/schema_list.json`) when we added the new schema (v0.1.8)?
    ```
    {
        "version": "0.1.8",
        "filename": "brc_schema_0.1.8.json",
        "supported": false
    }
    ```
    Since we're now working on the UI, we want to set that flag to `true` so that data sets conforming to schema 0.1.8 show up in the user interface:
    ```
    {
        "version": "0.1.8",
        "filename": "brc_schema_0.1.8.json",
        "supported": true
    }
    ```

12. Adding support for a new schema in the User Interface.

    In the UI code, add schema 0.1.8 to the version component map (`client/src/views/datasets/versionComponentMap.js`). I'll outline a few different cases (A - D) below as examples.

    For breaking changes, new views are implemented so that old dataset (e.g., 0.0.4 - 0.0.8) and newer data sets (e.g., 0.1.0 - 0.1.7) can be supported by the app at the same time. We had an instance of that a few months ago, where we had the following views:
    - `client/src/views/datasets/Dataset_0_0_8.vue`
    - `client/src/views/datasets/Dataset_0_1_0.vue`

    The new view (in that case) was created to support a change in the cardinality or depth of some field (I don't recall which one). The version number in the names indicate "schema 0.0.8 compatible" and "schema 0.1.0 compatible" respectively. Other than that, the version number doesn't really indicate the first or last version that is supported by the view. **Note:** We never used schema versions 0.0.6, 0.0.9, 0.1.5-0.1.6.

    **A. Multiple views are needed for schemas that contain breaking changes.**

    In that scenario outlined above, we would have seen the following in `versionComponentMap.js`:
    ```
    import Dataset_0_0_8 from "./Dataset_0_0_8.vue";
    import Dataset_0_1_0 from "./Dataset_0_1_0.vue";
    
    const versionMappings = [
      { versions: ['default', '0.0.4', '0.0.5', '0.0.7', '0.0.8'], component: Dataset_0_0_8 },
      { versions: ['default', '0.1.0', '0.1.1', '0.1.2'], component: Dataset_0_1_0 }
    ];
    ```
    But after all of the data feeds had updated to schema 0.1.0 (or later), we were able to remove support for those older schemas (and thus also remove the older `Dataset_0_0_8` view that was no longer in use.

    **B. Sometimes only a single view is necessary.**

    The `versionComponentMap.js` now looks like this, where we only need a single view to support all schemas currently in use:
    ```
    import Dataset_0_1_0 from "./Dataset_0_1_0.vue";
    
    const versionMappings = [
      { versions: ['default', '0.1.0', '0.1.1', '0.1.2', '0.1.3', '0.1.4', '0.1.7'], component: Dataset_0_1_0 }
    ];
    ```

    **C. Testing a new schema for breaking changes in the UI.**

    When testing the existing UI view (`Dataset_0_1_0.vue`) with version 0.1.8, simply add that version to the latest view:
    ```
    import Dataset_0_1_0 from "./Dataset_0_1_0.vue";
    
    const versionMappings = [
      { versions: ['default', '0.1.0', '0.1.1', '0.1.2', '0.1.3', '0.1.4', '0.1.7', '0.1.8'], component: Dataset_0_1_0 }
    ];
    ```

    **D. Adding support for a new view to accommodate a breaking change.**

    As in case A above, if you discover that schema 0.1.8 contains a breaking change, then you would instead create a new view, like this:
    ```
    import Dataset_0_1_0 from "./Dataset_0_1_0.vue";
    import Dataset_0_1_8 from "./Dataset_0_1_8.vue";
    
    const versionMappings = [
      { versions: ['default', '0.1.0', '0.1.1', '0.1.2', '0.1.3', '0.1.4', '0.1.7'], component: Dataset_0_1_0 },
      { versions: ['0.1.8'], component: Dataset_0_1_8 }
    ];
    ```
    Then, of course, copy `client/src/views/datasets/Dataset_0_1_0.vue` to `client/src/views/datasets/Dataset_0_1_8.vue` and modify `Dataset_0_1_8.vue` to handle whatever breaking changes were introduced in schema 0.1.8.

    **Note:** The `default` schema was introduced when we added support for schema 0.1.8. This version of the schema was the first to require the BRC data feeds to indicate which schema_version they were intended to comply with. Since each BRC adopted this schema version at a different time, we introduced the concept of a `default` view that would be applied if a data feed did not have a `schema_version` field. This, then, is a relic that will likely be removed at some point in the future.

13. Build the app and run the import against a clean database instance.

    a. Delete any local docker containers for the bioenergy.org PostgreSQL instance and app (I just do this via Docker Desktop). _We do this because we need a clean database to load the feeds into._

    b. In one shell, start the database docker image and build/run the server:

    ```
    docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 6432:5432 postgres
    docker-compose up --build
    ```

    c. When the server is up and running (you'll see `Server is running on port 8080.`), run the import code in a different shell:

    ```
    docker compose run api node scripts/import_datafeeds.js 2>&1 > import_datafeeds.txt
    ```

14. Testing the UI for compatibility with an existing view or a new view.

    Test the (un-modified) user interface to see whether records corresponding to schema 0.1.8 break the user interface.

    This involves viewing one of what are usually a handful of new records that prompted the schema change. These records are usually indicated in the issue that prompted the schema change in the brc-schema repo. If there are any questions about which records you should be examining, consult with the maintainer of the brc-schema repo.

15. If/when everything looks correct, commit your changes and create a PR:

    - `api/app/schemas/schema_list.json` (if you changed a `supported` flag for a schema)
    - `client/src/views/datasets/versionComponentMap.js`
    - `client/src/views/datasets/Dataset_0_1_8.vue` (i.e., if you needed to create a new for schema 0.1.8)

### Phase 3. Retiring unused schemas.

16. Determine which schemas can be retired.

    If you recall, back in Phase 1 step 6, you checked which schemas are currently in use and found that among the four data feeds, schema versions 0.1.1, 0.1.2, 0.1.4, and 0.1.7 were in use. In Phase 1 steps 3-5 and Phase 2 steps 11-12 you added server support for schema 0.1.8. Let's assume that GLBRC updated their data feed to version 0.1.8, so that the following schemas are now in use:

    - 0.1.1
    - 0.1.2
    - 0.1.4
    - 0.1.8

    You can, of course, check which schemas are in use at any given time using the URLs in `api/app/config/datafeeds.json`. But let's assume specifically the above 4 schemas are the ones in use, and that schema 0.1.8 required a new UI view to be implemented (this would be Phase 2 case 12 D above), so the current `api/app/schemas/schema_list.json` looks like this:

    ```
    [{
        "version": "0.1.0",
        "filename": "brc_schema_0.1.0.json",
        "supported": true
    },{
        "version": "0.1.1",
        "filename": "brc_schema_0.1.1.json",
        "supported": true
    },{
        "version": "0.1.2",
        "filename": "brc_schema_0.1.2.json",
        "supported": true
    },{
        "version": "0.1.3",
        "filename": "brc_schema_0.1.3.json",
        "supported": true
    },{
        "version": "0.1.4",
        "filename": "brc_schema_0.1.4.json",
        "supported": true
    },{
        "version": "0.1.7",
        "filename": "brc_schema_0.1.7.json",
        "supported": true
    },{
        "version": "0.1.8",
        "filename": "brc_schema_0.1.8.json",
        "supported": true
    }
    ]
    ```

    and the current `versionComponentMap.js` looks like this:

    ```
    import Dataset_0_1_0 from "./Dataset_0_1_0.vue";
    import Dataset_0_1_8 from "./Dataset_0_1_8.vue";
    
    const versionMappings = [
      { versions: ['default', '0.1.0', '0.1.1', '0.1.2', '0.1.3', '0.1.4', '0.1.7'], component: Dataset_0_1_0 },
      { versions: ['0.1.8'], component: Dataset_0_1_8 }
    ];
    ```

17. Remove UI support for unused schemas.

    a. Update the version component map.

    In `client/src/views/datasets/versionComponentMap.js` simply remove any references to schemas that are not in use. In our example we would remove schemas 0.1.0, 0.1.3, and 0.1.7:
    ```
    import Dataset_0_1_0 from "./Dataset_0_1_0.vue";
    import Dataset_0_1_8 from "./Dataset_0_1_8.vue";
    
    const versionMappings = [
      { versions: ['default', '0.1.1', '0.1.2', '0.1.4'], component: Dataset_0_1_0 },
      { versions: ['0.1.8'], component: Dataset_0_1_8 }
    ];
    ```

    b. Remove references to any unused views.

    If we were removing a view, we'd be deleting the import and the corresponding element of the version mappings array.
    **Note:** In this example, we still have three schemas using the `Dataset_0_1_0` view and one schema using the `Dataset_0_1_8` view, so there is nothing for us to do this time.

    c. Delete the .vue file for any unused views.

        **Note:** In this example, both views are still in use, so we need to keep both `client/src/views/datasets/Dataset_0_1_0.vue` and `client/src/views/datasets/Dataset_0_1_0.vue`.

18. Remove server support for any unused schemas.

    Continuing the same example...

    a. Remove references to any unused schemas from `api/app/schemas/schema_list.json`.

    For our example, that would look like this:

    ```
    [{
        "version": "0.1.1",
        "filename": "brc_schema_0.1.1.json",
        "supported": true
    },{
        "version": "0.1.2",
        "filename": "brc_schema_0.1.2.json",
        "supported": true
    },{
        "version": "0.1.4",
        "filename": "brc_schema_0.1.4.json",
        "supported": true
    },{
        "version": "0.1.8",
        "filename": "brc_schema_0.1.8.json",
        "supported": true
    }
    ]
    ```

    b. Delete any unused schema files.

    In our example, we would delete:

    - `api/app/schemas/brc_schema_0.1.0.json`
    - `api/app/schemas/brc_schema_0.1.3.json`
    - `api/app/schemas/brc_schema_0.1.7.json`

18. Build and test the import (same as Phase 2 step 13).

20. Test the User Interface (same as Phase 2 step 14).

21. Commit the changed files and create a PR.

    - `api/app/schemas/brc_schema_0.1.0.json`
    - `api/app/schemas/brc_schema_0.1.3.json`
    - `api/app/schemas/brc_schema_0.1.7.json`
    - `api/app/schemas/schema_list.json`
    - `client/src/views/datasets/versionComponentMap.js`
    - and, of course, any .vue files that are no longer need (nothing to do for this example)

That's it. You're done!