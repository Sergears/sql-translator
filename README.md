# Natural language to SQL translator

-   This app is an easy-to-use interface for English to SQL translation, built on top [Hugging Face](https://huggingface.co/docs/transformers/index) transformer library
-   Current baseline model is by [juierror](https://huggingface.co/juierror/text-to-sql-with-table-schema), more models are to be added
-   Example: 
    - Question `Show who won the 1962 prize for literature`
    - Table columns
        - `year`
        - `subject`
        - `winner` 
    - Result: `SELECT winner FROM table WHERE year = 1962 AND subject = literature`
-   Try it yourself 😊
