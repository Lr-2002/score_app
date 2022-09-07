import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
#todo git 同步，部署，换端口
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


def change_df(df, tree):
    for i in range(df.shape[0]):
        for j in df.keys():
            if j == 'name':
                continue
            else:
                df.loc[i, j] = tree.loc[df.loc[i, 'name'], j]
    return df

def show_admin_super(df):
    tree = df.set_index('name')
    change_list = ['score', 'reason','mod', 'sc']
    show_dict={'score':'分数','reason':'扣分原因', 'mod':'权限等级','sc':'密码'}
    st.selectbox('姓名',df['name'], key='select_name')
    for i in change_list:
        # st.text(i+':    '+str(tree.loc[session_state.select_name, i]))
        st.text_input(show_dict[i]+':    '+str(tree.loc[session_state['select_name'], i]), key = 'select_'+i)
    st.write('权限等级：最高级管理员：2 ，管理员：1，普通用户：0')
    st.button('确认提交',key='con')
    if session_state['con']:
        for i in change_list:
            temp = session_state['select_'+i]
            if temp != '':
                if i =='score':
                    tree.loc[session_state['select_name'], i ] = str(int(tree.loc[session_state['select_name'], i ])+ int(temp))
                elif  i=='reason':
                    tree.loc[session_state['select_name'], i ] += ';' + temp
                else:
                    tree.loc[session_state['select_name'], i ] = temp


        st.success('提交成功')
        change = change_df(df, tree)
        change.to_excel('./user.xlsx', index=False)
        show_df = tree[change_list]
        show_df= show_df.rename(columns=show_dict)

        st.dataframe(show_df)



def show_admin(df):
    tree = df.set_index('name')
    change_list = ['score', 'reason']
    show_dict={'score':'分数','reason':'扣分原因'}

    st.selectbox('姓名',df['name'], key='select_name')
    for i in change_list:
        # st.text(i+':    '+str(tree.loc[session_state.select_name, i]))
        st.text_input(show_dict[i]+':    '+str(tree.loc[session_state['select_name'], i]), key = 'select_'+i)
    st.button('确认提交',key='con')
    if session_state['con']:
        for i in change_list:
            temp = session_state['select_'+i]
            if temp != '':
                if i =='score':
                    tree.loc[session_state['select_name'], i ] = str(int(tree.loc[session_state['select_name'], i ])+ int(temp))
                elif  i=='reason':
                    tree.loc[session_state['select_name'], i ] += ';' + temp

        st.success('提交成功')
        change = change_df(df, tree)
        change.to_excel('./user.xlsx', index=False)
        show_df = tree[change_list]
        show_df =show_df.rename(columns=show_dict)
        st.dataframe(show_df)
        # print(change)
def try_or_none(name):
    p = ''
    try :
        p = session_state[name]
    except:
        p = ''
    return  p



def change_sc(sc):
    sc0 = try_or_none('sc0')
    sc1 = try_or_none('sc1')
    sc2 = try_or_none('sc2')


    sc0 = st.text_input('请输入原密码',value=sc0,  key='sc0')
    sc1 = st.text_input('请输入新密码',value=sc1, key='sc1')
    sc2 = st.text_input('确认新密码',value=sc2, key='sc2')
    if session_state['sc0'] == sc:
        change_scc = st.button('确认修改密码')
        # if change_scc :
        #     session_state['change_scc'] = True
        # # print(session_state['change_scc'])
        # if 'change_scc' in session_state.keys() and session_state['change_scc']:
        #     print(1)
        #     if session_state['sc1'] == session_state['sc2'] and session_state['sc1'] != '':
        #         st.success('密码修改成功')


df = pd.read_excel('./user.xlsx', dtype=str)
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
        session_state['mod'] = int(k)
        print(session_state['mod'], k)
        break
    else:
        # session_state['login'] = False
        continue
        # st.warning('密码错误，请重新登录')
if 'login' in session_state.keys() and session_state['login'] :
    if 'mod' in session_state.keys():
        if session_state['mod']  == 1:
            show_admin(df)
        elif session_state['mod'] ==0:
            show(name, df)
        elif  session_state['mod'] ==2 :
            show_admin_super(df)

