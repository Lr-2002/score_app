import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

session_state = st.session_state

def show(name, df):
    score, reason = None, None
    if 'score' in session_state.keys():
        score = session_state['score']
        reason = session_state['reason']
    if score is None:
        for i, j, k in zip(df['name'], df['score'], df['reason']):
            if i == name:
                score = j
                reason = k
                break
    session_state['score'] = score
    session_state['reason'] = reason
    st.title('你的得分是')
    st.text(session_state['score'])
    st.title('丢分原因是')
    st.text(session_state['reason'])


def show_admin(df):
    gb = GridOptionsBuilder.from_dataframe(df)

    # for i in df.keys():
    #     if '比例' in i:
    #         gb.configure_column(i, cellStyle= cells_jscode)
    #     elif '总成本' in i:
    #         gb.configure_column(i, editable=True)
    for i in df.keys():
        gb.configure_column(i, editable=True)
    gridOptions = gb.build()

    data = AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        try_to_convert_back_to_original_types=True,
        update_mode='value_changed'
        # editable=True
    )
    changeing = st.button('提交修改',key='changeing')
    if session_state.changeing:
        session_state['changed_data'] = data['data']
        st.success('提交成功')
        st.write(session_state['changed_data'])
        # session_state['changed_data'].to_csv('./add_on/total.', encoding='gbk', index=False)
        session_state['changed_data'].to_excel('./user.xlsx', index=False)



df = pd.read_excel('./user.xlsx')
# tree = df.set_index('name')
# print(df)


st.title('登录')
name = st.text_input('姓名', key='name')
sc = st.text_input('密码', key='sc')
# session_state['login'] = False

for i, j, k in zip(df['name'], df['sc'], df['mod']):
    if i == name and str(sc) == str(j):
        st.success('登录成功')
        session_state['login'] = True
        session_state['mod'] = bool(k)
        break
    else:
        st.warning('密码错误，请重新登录')
if 'login' in session_state.keys() and session_state['login'] :
    if not session_state['mod']:
        show(name, df)
    else:
        show_admin(df)

