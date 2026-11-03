const statusEl = document.getElementById("status");
const rowsEl = document.getElementById("linhas");
const selectEl = document.getElementById("jogo");
let supabaseClient;

function dinheiro(valor) {
  return Number(valor).toLocaleString("pt-BR", {style:"currency", currency:"BRL"});
}
function tempo(valor) {
  const total = Math.floor(Number(valor));
  return `${String(Math.floor(total/60)).padStart(2,"0")}:${String(total%60).padStart(2,"0")}`;
}
function data(valor) {
  return new Date(valor).toLocaleString("pt-BR");
}
async function iniciar() {
  if (!window.SUPABASE_URL || !window.SUPABASE_ANON_KEY ||
      window.SUPABASE_URL.includes("SEU-PROJETO")) {
    statusEl.textContent = "Configure site/config.js com a URL e a chave anon do Supabase.";
    return;
  }
  supabaseClient = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
  try {
    const {data, error} = await supabaseClient.from("jogos").select("id,nome").order("nome");
    if (error) throw error;
    selectEl.innerHTML = "";
    data.forEach(j => {
      const option = document.createElement("option");
      option.value = j.id; option.textContent = j.nome; selectEl.appendChild(option);
    });
    if (!data.length) { statusEl.textContent = "Nenhum jogo cadastrado."; return; }
    selectEl.value = window.JOGO_ID || data[0].id;
    await carregar();
  } catch (e) { statusEl.textContent = "Falha ao consultar os jogos: " + e.message; }
}
async function carregar() {
  if (!supabaseClient) return;
  statusEl.textContent = "Atualizando...";
  rowsEl.innerHTML = "";
  try {
    const {data, error} = await supabaseClient.from("ranking")
      .select("id,jogo_id,apelido,valor_ganho,tempo_segundos,data_hora")
      .eq("jogo_id", selectEl.value)
      .order("valor_ganho", {ascending:false})
      .order("tempo_segundos", {ascending:true})
      .order("data_hora", {ascending:true})
      .order("id", {ascending:true})
      .limit(10);
    if (error) throw error;
    if (!data.length) { statusEl.textContent = "Ainda não existem resultados para este jogo."; return; }
    data.forEach((p, i) => {
      const tr = document.createElement("tr");
      [i+1, selectEl.selectedOptions[0]?.textContent || "Show do Milhão", p.apelido, dinheiro(p.valor_ganho), tempo(p.tempo_segundos), dataFormatada(p.data_hora)]
        .forEach(v => { const td=document.createElement("td"); td.textContent=v; tr.appendChild(td); });
      rowsEl.appendChild(tr);
    });
    statusEl.textContent = `Exibindo ${data.length} melhor(es) resultado(s) deste jogo.`;
  } catch(e) { statusEl.textContent = "Não foi possível carregar o ranking: " + e.message; }
}
function dataFormatada(v) { return new Date(v).toLocaleString("pt-BR"); }
document.getElementById("atualizar").addEventListener("click", carregar);
selectEl.addEventListener("change", carregar);
iniciar();
