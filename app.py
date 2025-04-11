import streamlit as st
import requests

# --- BARRE LATÉRALE ---
st.sidebar.title("📚 POC Base documentaire IFA")

# Texte descriptif
st.sidebar.write(
    "Cette application vous permet de consulter et d'interroger la base documentaire "
    "d'IFA"
)

# Exemple de documents à lister dans la sidebar
# À adapter selon la structure de vos propres documents (titres, URL, etc.)
documents_tcm = [
    {"title": "Les systèmes d'intelligence artificielle et les conseils d'administration.pdf", "url": ""},
  ]

st.sidebar.markdown("### Documents disponibles")
for doc in documents_tcm:
    st.sidebar.markdown(f"- [{doc['title']}]({doc['url']})")

st.sidebar.markdown("---")

st.sidebar.write(
    "Pour la phase de test, uniquement les documents ci-dessus sont disponibles."
    )

st.sidebar.write(
    "Méthode RAG (Contextual Retriving)"
    )

# -- INITIALISATION --
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.title("📚 IFA Chatbot 🤖")
st.text("Testez le chatbot RAG en fonction des éléments présents dans les documents")

# 1) Récupérer la question AVANT l’affichage
user_input = st.chat_input("Posez votre question ici…")

if user_input:
    # On ajoute le message "user" à l'historique
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # 2) APPEL À N8N (webhook) pour récupérer la réponse RAG
    #    Adaptez l’URL à votre configuration (webhook test vs production)
    #    Ex: http://localhost:5678/webhook/rag
    try:
        response = requests.post(
            "https://n8n.srv749429.hstgr.cloud/webhook-test/96ab6917-eba1-47c1-80cb-d4be6da6a364",
            json={"question": user_input},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()

            # On suppose que n8n renvoie un JSON de type {"answer": "..."}
            rag_answer = data.get("answer", "Aucune réponse trouvée.")
        else:
            rag_answer = f"Erreur (code {response.status_code}) lors de la requête."
    except requests.exceptions.RequestException as e:
        rag_answer = f"Erreur de connexion à n8n: {e}"

    # On ajoute la réponse "assistant"
    st.session_state.conversation.append({"role": "assistant", "content": rag_answer})

# 3) AFFICHER TOUTE LA CONVERSATION
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
