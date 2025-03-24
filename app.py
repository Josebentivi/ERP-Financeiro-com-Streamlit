import streamlit as st
import pandas as pd
import sqlite3
import datetime

def main():
    st.title("ERP Financeiro com Streamlit")

    # Atualização do menu de opções – foram adicionadas novas funcionalidades.
    menu = [
        "Clientes",
        "Contas a Pagar",
        "Contas a Receber",
        "Lançamentos",
        "Status Contas",
        "Top 5 Clientes",
        "Comparação Receita x Despesa"
    ]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)

    # Conexão com o banco de dados
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)

    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Status Contas":
        st.subheader("Status das Contas a Pagar e Receber")
        st.markdown("Contas a Pagar:")
        df_pagar = pd.read_sql_query(
            "SELECT status, COUNT(*) as count, SUM(valor) as total_valor FROM contas_pagar GROUP BY status", conn)
        st.dataframe(df_pagar)
        st.bar_chart(df_pagar.set_index("status")["total_valor"])
        
        st.markdown("Contas a Receber:")
        df_receber = pd.read_sql_query(
            "SELECT status, COUNT(*) as count, SUM(valor) as total_valor FROM contas_receber GROUP BY status", conn)
        st.dataframe(df_receber)
        st.bar_chart(df_receber.set_index("status")["total_valor"])
        
    elif choice == "Top 5 Clientes":
        st.subheader("Top 5 Clientes com Maior Receita")
        query = """
            SELECT c.nome, SUM(cr.valor) as total_receita
            FROM contas_receber cr
            JOIN clientes c ON cr.cliente_id = c.id
            WHERE cr.status = 'Recebido'
            GROUP BY c.nome
            ORDER BY total_receita DESC
            LIMIT 5
        """
        df_top5 = pd.read_sql_query(query, conn)
        st.dataframe(df_top5)
        if not df_top5.empty:
            st.bar_chart(df_top5.set_index("nome")["total_receita"])
            
    elif choice == "Comparação Receita x Despesa":
        st.subheader("Comparação Receita vs Despesa (Mês Atual)")
        # Obtém o mês atual no formato 'YYYY-MM'
        current_month = datetime.date.today().strftime('%Y-%m')
        df_lanc = pd.read_sql_query("SELECT * FROM lancamentos", conn, parse_dates=["data"])
        df_lanc['month'] = df_lanc['data'].dt.strftime('%Y-%m')
        df_current = df_lanc[df_lanc['month'] == current_month]
        df_comparacao = df_current.groupby("tipo")["valor"].sum().reset_index()
        st.dataframe(df_comparacao)
        st.bar_chart(df_comparacao.set_index("tipo")["valor"])
        
    conn.close()
    
if __name__ == "__main__":
    main()
