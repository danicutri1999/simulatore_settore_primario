import random
from datetime import datetime


class SimulatoreProduzioneZioPeppe:
    """
    Classe principale per simulare il processo produttivo dell'azienda agricola
    e di trasformazione "Zio Peppe" che si occupa di allevamento e produzione
    di carni, salumi e formaggi.
    """

    def __init__(self):
        """
        Inizializza il simulatore con le configurazioni di default per i vari
        prodotti e processi produttivi dell'azienda.
        """
        # Configurazione prodotti (3 tipologie principali richieste)
        self.prodotti = {
            'carne_bovina': {
                'nome': 'Carne Bovina',
                'tempo_per_kg': 0.15,  # ore per kg (macellazione + lavorazione)
                'capacita_giornaliera': 500,  # kg al giorno
                'unita_misura': 'kg'
            },
            'carne_suina': {
                'nome': 'Carne Suina',
                'tempo_per_kg': 0.12,  # ore per kg
                'capacita_giornaliera': 400,  # kg al giorno
                'unita_misura': 'kg'
            },
            'salumi': {
                'nome': 'Salumi',
                'tempo_per_kg': 0.25,  # ore per kg (lavorazione + stagionatura iniziale)
                'capacita_giornaliera': 200,  # kg al giorno
                'unita_misura': 'kg'
            },
            'formaggi': {
                'nome': 'Formaggi',
                'tempo_per_kg': 0.20,  # ore per kg
                'capacita_giornaliera': 150,  # kg al giorno
                'unita_misura': 'kg'
            }
        }

        # Sequenze produttive (2 sequenze differenti richieste)
        self.sequenze = {
            'sequenza_macellazione': ['carne_bovina', 'carne_suina'],
            'sequenza_trasformazione': ['salumi', 'formaggi']
        }

        # Quantità da produrre (inizialmente vuote, generate casualmente)
        self.quantita_produzione = {}

    def genera_quantita_casuali(self, min_qty=50, max_qty=300):
        """
        Genera casualmente le quantità da produrre per ogni tipo di prodotto.

        Args:
            min_qty (int): Quantità minima da produrre (default 50 kg)
            max_qty (int): Quantità massima da produrre (default 300 kg)

        Returns:
            dict: Dizionario con le quantità generate per ogni prodotto
        """
        print("=" * 60)
        print("GENERAZIONE QUANTITÀ DI PRODUZIONE")
        print("=" * 60)

        for codice_prodotto, info in self.prodotti.items():
            quantita = random.randint(min_qty, max_qty)
            self.quantita_produzione[codice_prodotto] = quantita
            print(f"• {info['nome']}: {quantita} {info['unita_misura']}")

        print()
        return self.quantita_produzione

    def configura_tempo_produzione(self, prodotto, tempo_per_unita):
        """
        Configura il tempo di produzione per unità di un prodotto specifico.

        Args:
            prodotto (str): Codice del prodotto da configurare
            tempo_per_unita (float): Tempo in ore per unità di prodotto
        """
        if prodotto in self.prodotti:
            self.prodotti[prodotto]['tempo_per_kg'] = tempo_per_unita
            print(f"✓ Tempo di produzione per {self.prodotti[prodotto]['nome']} "
                  f"aggiornato a {tempo_per_unita} ore/{self.prodotti[prodotto]['unita_misura']}")
        else:
            print(f"✗ Prodotto '{prodotto}' non trovato")

    def configura_capacita_giornaliera(self, prodotto, capacita):
        """
        Configura la capacità produttiva massima giornaliera per un prodotto.

        Args:
            prodotto (str): Codice del prodotto da configurare
            capacita (int): Capacità massima in kg al giorno
        """
        if prodotto in self.prodotti:
            self.prodotti[prodotto]['capacita_giornaliera'] = capacita
            print(f"✓ Capacità giornaliera per {self.prodotti[prodotto]['nome']} "
                  f"aggiornata a {capacita} {self.prodotti[prodotto]['unita_misura']}/giorno")
        else:
            print(f"✗ Prodotto '{prodotto}' non trovato")

    def configura_capacita_complessiva(self, capacita_totale):
        """
        Configura la capacità produttiva complessiva dell'azienda considerando
        tutte le linee produttive insieme.

        Args:
            capacita_totale (int): Capacità massima totale in kg al giorno
        """
        self.capacita_complessiva = capacita_totale
        print(f"✓ Capacità produttiva complessiva impostata a {capacita_totale} kg/giorno")

    def calcola_tempo_produzione(self, prodotto, quantita):
        """
        Calcola il tempo necessario per produrre una determinata quantità di un prodotto,
        considerando i vincoli di capacità giornaliera.

        Args:
            prodotto (str): Codice del prodotto
            quantita (float): Quantità da produrre

        Returns:
            dict: Dizionario con tempi di produzione e informazioni dettagliate
        """
        info_prodotto = self.prodotti[prodotto]
        tempo_per_unita = info_prodotto['tempo_per_kg']
        capacita_giornaliera = info_prodotto['capacita_giornaliera']

        # Calcolo giorni necessari considerando la capacità giornaliera
        giorni_necessari = quantita / capacita_giornaliera

        # Tempo effettivo di lavorazione (ore)
        tempo_lavorazione = quantita * tempo_per_unita

        # Se la produzione supera la capacità giornaliera, si distribuisce su più giorni
        if quantita > capacita_giornaliera:
            giorni_effettivi = int(quantita / capacita_giornaliera) + (1 if quantita % capacita_giornaliera > 0 else 0)
        else:
            giorni_effettivi = 1

        return {
            'prodotto': info_prodotto['nome'],
            'quantita': quantita,
            'tempo_lavorazione_ore': round(tempo_lavorazione, 2),
            'tempo_lavorazione_giorni': round(giorni_necessari, 2),
            'giorni_effettivi': giorni_effettivi,
            'tempo_totale_ore': round(giorni_effettivi * 8, 2)  # 8 ore lavorative al giorno
        }

    def simula_sequenza_produttiva(self, nome_sequenza):
        """
        Simula l'intera sequenza produttiva per un gruppo di prodotti correlati,
        calcolando i tempi complessivi e le informazioni dettagliate.

        Args:
            nome_sequenza (str): Nome della sequenza da simulare

        Returns:
            dict: Risultati della simulazione con tempi totali
        """
        if nome_sequenza not in self.sequenze:
            print(f"✗ Sequenza '{nome_sequenza}' non trovata")
            return None

        print("=" * 60)
        print(f"SIMULAZIONE SEQUENZA: {nome_sequenza.upper().replace('_', ' ')}")
        print("=" * 60)

        risultati = []
        tempo_totale_ore = 0
        tempo_totale_giorni = 0

        for prodotto in self.sequenze[nome_sequenza]:
            if prodotto not in self.quantita_produzione:
                print(f"⚠ Quantità non definita per {prodotto}, salto...")
                continue

            quantita = self.quantita_produzione[prodotto]
            risultato = self.calcola_tempo_produzione(prodotto, quantita)
            risultati.append(risultato)

            # Aggiorno i totali
            tempo_totale_ore += risultato['tempo_lavorazione_ore']
            tempo_totale_giorni = max(tempo_totale_giorni, risultato['giorni_effettivi'])

            # Stampo i dettagli
            print(f"\n{risultato['prodotto']}:")
            print(f"  • Quantità: {risultato['quantita']} kg")
            print(f"  • Tempo lavorazione: {risultato['tempo_lavorazione_ore']} ore")
            print(f"  • Giorni necessari: {risultato['giorni_effettivi']} giorni")

        print(f"\n{'─' * 60}")
        print(f"TOTALE SEQUENZA:")
        print(f"  • Tempo lavorazione totale: {round(tempo_totale_ore, 2)} ore")
        print(f"  • Giorni produttivi totali: {tempo_totale_giorni} giorni")
        print(f"  • Ore medie al giorno: {round(tempo_totale_ore / max(tempo_totale_giorni, 1), 2)} ore/giorno")
        print()

        return {
            'sequenza': nome_sequenza,
            'dettagli_prodotti': risultati,
            'tempo_totale_ore': round(tempo_totale_ore, 2),
            'giorni_totali': tempo_totale_giorni,
            'ore_medie_giorno': round(tempo_totale_ore / max(tempo_totale_giorni, 1), 2)
        }

    def rapporto_produzione_completo(self):
        """
        Genera un rapporto completo della produzione simulata per tutti i prodotti,
        includendo entrambe le sequenze produttive e i tempi totali.

        Returns:
            dict: Rapporto completo con tutti i risultati
        """
        print("\n" + "=" * 60)
        print("RAPPORTO PRODUZIONE COMPLETO - MACELLERIA ZIOPEPPE")
        print("=" * 60)
        print(f"Data simulazione: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print()

        rapporto = {
            'data_simulazione': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'quantita_produzione': self.quantita_produzione.copy(),
            'sequenze': {}
        }

        # Simulo entrambe le sequenze
        for nome_sequenza in self.sequenze.keys():
            risultato_sequenza = self.simula_sequenza_produttiva(nome_sequenza)
            rapporto['sequenze'][nome_sequenza] = risultato_sequenza

        # Calcolo totali generali
        tempo_totale_generale = sum(
            seq['tempo_totale_ore']
            for seq in rapporto['sequenze'].values()
            if seq is not None
        )

        giorni_totali_generale = max(
            seq['giorni_totali']
            for seq in rapporto['sequenze'].values()
            if seq is not None
        )

        print("=" * 60)
        print("RIEPILOGO GENERALE PRODUZIONE")
        print("=" * 60)
        print(f"Tempo lavorazione totale: {round(tempo_totale_generale, 2)} ore")
        print(f"Giorni produttivi necessari: {giorni_totali_generale} giorni")
        print(f"Ore medie giornaliere: {round(tempo_totale_generale / max(giorni_totali_generale, 1), 2)} ore/giorno")

        # Quantità totali
        quantita_totale = sum(self.quantita_produzione.values())
        print(f"Quantità totale prodotta: {quantita_totale} kg")
        print("=" * 60)
        print()

        rapporto['totali_generali'] = {
            'tempo_totale_ore': round(tempo_totale_generale, 2),
            'giorni_totali': giorni_totali_generale,
            'ore_medie_giorno': round(tempo_totale_generale / max(giorni_totali_generale, 1), 2),
            'quantita_totale_kg': quantita_totale
        }

        return rapporto


# ============================================================================
# ESEMPIO DI UTILIZZO DEL SIMULATORE
# ============================================================================

def main():
    """
    Funzione principale che esegue una simulazione completa del processo
    produttivo dell'azienda "Zio Peppe".
    """
    print("\n" + "🐄" * 30)
    print("SIMULATORE PROCESSO PRODUTTIVO")
    print("MACELLERIA BRACERIA 'ZIO PEPPE'")
    print("🐄" * 30 + "\n")

    # Creo l'istanza del simulatore
    simulatore = SimulatoreProduzioneZioPeppe()

    # Genero quantità casuali di produzione
    simulatore.genera_quantita_casuali(min_qty=80, max_qty=250)

    # Esempio di configurazione personalizzata (opzionale)
    print("\n" + "─" * 60)
    print("CONFIGURAZIONI PERSONALIZZATE (esempio)")
    print("─" * 60)
    simulatore.configura_tempo_produzione('carne_bovina', 0.18)
    simulatore.configura_capacita_giornaliera('salumi', 220)
    print()

    # Genero il rapporto completo
    rapporto = simulatore.rapporto_produzione_completo()

    # Informazioni aggiuntive
    print("\n" + "📊" * 30)
    print("ANALISI EFFICIENZA PRODUTTIVA")
    print("📊" * 30 + "\n")

    for sequenza, dati in rapporto['sequenze'].items():
        if dati:
            efficienza = (dati['ore_medie_giorno'] / 8) * 100  # % di utilizzo giornata lavorativa
            print(f"{sequenza.replace('_', ' ').title()}:")
            print(f"  Efficienza utilizzo giornata: {round(efficienza, 1)}%")

    print("\n" + "✓" * 60)
    print("SIMULAZIONE COMPLETATA CON SUCCESSO")
    print("✓" * 60 + "\n")


if __name__ == "__main__":
    main()