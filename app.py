import streamlit as st
import os
import tempfile


@st.cache_resource
def load_the_model():
    from anonymisation_hybride import hybrid_anonymiser

    return hybrid_anonymiser


# Use the imported module
hybrid_anonymiser = load_the_model()


# Streamlit App
def main():
    st.title("Anonymiseur de fichier")
    st.write("Chargez un fichier HTML, et nous l'anonymiserons pour vous.")

    # File upload
    uploaded_file = st.file_uploader("Chargez le fichier ici", type=["html"])

    if uploaded_file is not None:
        # Create a temporary file to save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Process the file with the anonymize function
        anonymized_file_path = temp_file_path.replace(".html", "_anonymized.html")
        hybrid_anonymiser(temp_file_path, anonymized_file_path)

        # Create a download button for the anonymized file
        with open(anonymized_file_path, "r", encoding="utf-8") as file:
            st.download_button(
                label="Télécharger le fichier anonymisé",
                data=file,
                file_name="fichier_anonymisé.html",
                mime="text/html",
            )

        # Cleanup the temporary files (optional)
        os.remove(temp_file_path)
        os.remove(anonymized_file_path)


if __name__ == "__main__":
    main()
