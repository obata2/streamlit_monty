import streamlit as st
import pandas as pd
import random
from PIL import Image

#選択してなく、かつ当たりでもないドアを1つ、_missにする
def chairman(doors_img, select_index, hit_index):
  open_index = random.randint(0, 2)
  while(open_index == select_index or open_index == hit_index):
    open_index = random.randint(0, 2)
  doors_img[open_index] = Image.open("assets\door_miss.png")
  st.session_state.open_index = open_index
  if open_index == 0:
    st.write("司会者は、左の扉 を開けました")
  elif open_index == 1:
    st.write("司会者は、中央の扉 を開けました")
  elif open_index == 2:
    st.write("司会者は、右の扉 を開けました")
  return doors_img
  
#選択を変更する  ->   select_indexではなく、open_indexでもない所に移る
def change(select_index):
  changedSelect_index = random.randint(0, 2)
  open_index = st.session_state.open_index
  while(changedSelect_index == select_index or changedSelect_index == open_index):
    changedSelect_index = random.randint(0, 2)
  return changedSelect_index

#ドアの画像を表示する
def show(doors_img, select_index):
  cursor = Image.open("assets\door_cursor.png")
  col1, col2, col3 = st.columns((1, 1, 1))
  with col1:
    st.image(doors_img[0])
    if select_index == 0:
      st.image(cursor)
  with col2:
    st.image(doors_img[1])
    if select_index == 1:
      st.image(cursor)
  with col3:
    st.image(doors_img[2])
    if select_index == 2:
      st.image(cursor)

#任意の回数のシミュレートを行い、当たりの回数をカウントしていく    ->  hit_index, select_index, open_index を用意する
def simulate(repeat, count):
  c1 = 0
  c2 = 0 
  for i in range(1, repeat+1):
    count[i][0] = c1
    count[i][1] = c2
    hit_index_sim = random.randint(0,2)
    select_index_sim = random.randint(0,2)
    open_index_sim = random.randint(0,2)
    while(open_index_sim == select_index_sim or open_index_sim == hit_index_sim):
      open_index_sim = random.randint(0,2)
    #選択を変えないときの正誤判定   ->  select と hit が一致しているか
    if select_index_sim == hit_index_sim:
      c2 += 1
      count[i][1] = c2
    #選択を変えるときの正誤判定     ->   selectではなく、openでもないところへ移動して一致するか
    changedSelect_index_sim = random.randint(0,2)
    while(changedSelect_index_sim == select_index_sim or changedSelect_index_sim == open_index_sim):
      changedSelect_index_sim = random.randint(0,2)
    if(changedSelect_index_sim == hit_index_sim):
      c1 += 1
      count[i][0] = c1
  return count


#ここから
st.markdown("# モンティホール問題を  \n# Pythonでシミュレーションする")
st.image("assets\MontyHall_illustration.jpg", use_column_width="auto")
st.write(
"""
## モンティホール問題とは？
アメリカのテレビ番組「Let's make a deal」で登場したゲームのことです。  
直観的に正しいと思う答えと、計算によって求められる正しい答えが食い違うパラドックスとして知られています。  
  
**ルール**  
プレイヤーは、始めに3つある扉のうち1つを選びます。1つの扉の向こうには賞品である車が(当たり)、残り2つの扉の向こうにはヤギがいます(外れ)。プレイヤーが扉を選択した後、司会者は外れの扉を1つ開けます。  
**このとき、あなたは最初に選んだ扉をそのまま開けるか、別の扉に変更するかを改めて選択することができます。あなたはどちらを選びますか？**
""")

st.write("## 実験してみる")
st.write("1. 始めに、扉を1つ選んでください。")
sel_1 = st.radio(
  "",
  ("左の扉", "中央の扉", "右の扉"),
  index = None,
  horizontal = True,
  label_visibility = "collapsed",
)
select_index = -1
if sel_1 == "左の扉":
  select_index = 0
elif sel_1 == "中央の扉":
  select_index = 1
elif sel_1 == "右の扉":
  select_index = 2

doors_img = [0]*3
doors_img[0] = Image.open("assets\door_closed.png")
doors_img[1] = Image.open("assets\door_closed.png")
doors_img[2] = Image.open("assets\door_closed.png")
#初期状態のみ実行される  -  3つ全て閉じた状態のドアの表示と、当たりドアの抽選
if sel_1 == None:
  hit_index = random.randint(0,2)
  st.session_state.hit_index = hit_index
  show(doors_img, select_index)
#
else:
  hit_index = st.session_state.hit_index
  doors_img = chairman(doors_img, select_index, hit_index)
  st.write("2. 選んだ扉を変更しますか？")
  sel_2 = st.radio(
    "",
    ("する", "しない"),
    index = None,
    horizontal = True,
    label_visibility = "collapsed",
  )
  #扉の変更の有無が入力されているとき
  if sel_2 == "する":
    select_index = change(select_index)
  #hit_index以外のドアは外れに、hit_indexは当たりに     ->   sel_2がNoneでないときのみ
  if sel_2 != None:
    for i in range(0, 3):
      if i != hit_index:
        doors_img[i] = Image.open("assets\door_miss.png")
      else:
        doors_img[i] = Image.open("assets\door_hit.png")
  show(doors_img, select_index)
  if sel_1 != None and sel_2 != None and select_index == hit_index:
    st.write("**当たりです！ おめでとうございます**")
  elif sel_1 != None and sel_2 != None and select_index != hit_index:
    st.write("**残念、外れでした**")

st.write(
  """
  ## プレイヤーはどうすべきか？
  司会者が扉を1つ開けた時、残りは当たりと外れが1つずつです。  
  「選んだ扉を変更しますか？」という質問に対して、直感的には「当たりも外れも1/2になるのだから、扉を変更することに意味はない」と思うかもしれません。  
  しかし、この問題には直感と異なる結論が存在します。  
  下にその解説と、シミュレーションを示します。
  """)
with st.expander("解説を見る"):
  st.write(
  """
  実は、「**選んだ扉を変更する方が、当たりの確率は高い**」というのがこの問題の答えです。  
  ポイントは、最終的に当たりの扉を選択するために、最初の時点でどの扉を選んでいなければならないのかを考えることです。  
  **変更する場合**:  
  司会者は必ず外れの扉を1つ開けるため、当たりと外れが1つずつの状態で扉を変更します。最初の時点で選んだ扉が外れであれば、必ず当たりの扉に乗り換えることができます。最初に選んだ扉が外れである確率が、ここで当たりを引く確率となるので、2/3の確率で当たりを引くことができます。  
  **変更しない場合**:  
  最初の時点で当たりの扉を選んでおくことで、最終的に賞品を手に入れることができます。最初に選んだ扉が当たりである確率が、ここで当たりを引く確率となるので、1/3の確率で当たりを引くことができます。  
  """)

with st.expander("シミュレーションする"):
  st.write("当たりの確率が異なることを、シミュレーションによって確かめることができます。")
  repeat = st.slider(
    "試行回数を選択してください",
    min_value = 100, max_value = 100000, value = 10000, step = 100
    )
  do = st.button("スタート")
  if do:
    count = [[0 for i in range(2)]for j in range(repeat+1)]
    count = simulate(repeat, count)
    chart_data = pd.DataFrame(count, columns = ["変更する", "変更しない"])
    st.line_chart(chart_data, x_label = "試行回数", y_label = "当たりの回数")