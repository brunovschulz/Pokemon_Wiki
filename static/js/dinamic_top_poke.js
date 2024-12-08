document.getElementById("attribute-select").addEventListener("change", function () {
    const attribute = this.value;
    console.log("Atributo selecionado:", attribute);
    fetch(`/get_attribute?attribute=${attribute}`)
        .then(response => {
            console.log("Resposta do servidor:", response);
            return response.json();
        })
        .then(data => {
            console.log("Dados recebidos:", data);
            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = ""; // Limpa resultados anteriores

            data.forEach(pokemon => {
                console.log("Gerando card para:", pokemon);
                // Criação do card
                const link = document.createElement("a");
                link.href = `/pokemon/${pokemon.id}`;
                link.className = "pokemon-card-link";

                const card = document.createElement("div");
                card.className = "pokemon-card";

                const img = document.createElement("img");
                img.src = `/static/images/${pokemon.id}.png`;
                img.alt = pokemon.name;

                const title = document.createElement("h3");
                title.textContent = `#${pokemon.id} - ${pokemon.name}`;

                const att = document.createElement("h3");
                att.textContent = `${pokemon.att_name}: ${pokemon.attribute}`;

                card.appendChild(img);
                card.appendChild(title);
                card.appendChild(att);

                link.appendChild(card);

                resultsDiv.appendChild(link);
            });
        })
        .catch(error => console.error("Erro ao buscar dados:", error));
});