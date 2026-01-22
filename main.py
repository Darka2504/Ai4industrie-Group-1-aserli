import os
import sys
import agent

def run_query(agent_executor, query, thread_id="thread-fr-1"):
    print("\n" + "="*60)
    print(f"❓ Question: {query}")
    print("="*60)
    
    config_dict = {"configurable": {"thread_id": thread_id}}

    try:
        response = agent_executor.invoke(
            {"messages": [("user", query)]},
            config=config_dict,
        )

        # Display Answer
        print("\n🧠 Réponse de l'agent :")
        if response["messages"]:
            print(response["messages"][-1].content)
        else:
            print("⚠️ Pas de réponse générée.")

        # Verification Logic
        print("\n🔍 --- Vérification de l'utilisation de l'outil ---")
        has_used_tool = False
        for msg in response["messages"]:
            if msg.type == "tool":
                # Print a preview of what the tool found
                print(f"✅ L'agent a lu le PDF. Extrait : {str(msg.content)}...")
                has_used_tool = True

        if not has_used_tool:
            print("❌ ATTENTION : L'agent a répondu sans lire le fichier !")

    except Exception as e:
        print(f"❌ Une erreur est survenue lors de l'exécution de la requête : {e}")

def main():
 
    # 4. Run Queries
    questions = [
        "Quels sont les risques naturels et technologiques majeurs recensés dans le département de la Vienne selon le DDRM ?",
        "Quelles sont les principales rivières concernées par le risque inondation dans la Vienne et quels types d'inondations peuvent survenir ?",
        "Comment est classé le département de la Vienne en termes de zonage sismique ?",
        "Quelles sont les mesures de pré-distribution de comprimés d'iode prévues autour de la centrale nucléaire de Civaux ?",
        "Quels sont les établissements classés SEVESO seuil haut dans le département de la Vienne et où sont-ils situés ?",
        "De quoi se compose le Signal National d'Alerte et comment reconnaît-on le signal de fin d'alerte ?"
    ]

    for q in questions:
        run_query(agent_executor, q)

if __name__ == "__main__":
    main()