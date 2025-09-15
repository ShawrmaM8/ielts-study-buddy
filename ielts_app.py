import streamlit as st
import passage_utils as utils
import passage_summarizer as summarizer
import eng_flashcards as flashcards
import lang_feedback

st.set_page_config(page_title='IELTS Study Buddy', layout='wide')
st.title("📚 Study Assistant: IELTS Quiz & Flashcards")

# --- File Upload ---
uploaded_file = st.file_uploader('Upload your passage', type=['pdf', 'txt', 'docx'])

if uploaded_file is not None:
    try:
        # Extract text once and persist in session
        text = utils.extract_text(uploaded_file)
        st.session_state['passage_text'] = text

        st.write('### Extracted Passage')
        # Show first 1000 chars with option to expand
        if len(text) > 1000:
            with st.expander("View Full Passage (Click to Expand)"):
                st.write(text)
            st.write(text[:1000] + "...")
        else:
            st.write(text)

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please make sure you're uploading a valid PDF, DOCX, or TXT file.")
        st.stop()  # Stop execution if file processing fails

    # --- Summarization ---
    st.subheader('📝 Summary')
    try:
        @st.cache_data
        def get_summary(_text):
            return summarizer.summarize_text(_text)


        summary = get_summary(text)
        if summary:
            for s in summary:
                st.write("- " + s)
        else:
            st.info("No summary could be generated for this text.")

    except Exception as e:
        st.error(f"❌ Error generating summary: {str(e)}")

    # --- Flashcards / Quiz Generation ---
    st.subheader("📋 Flashcards & Quiz")
    try:
        @st.cache_data
        def get_flashcards(_text):
            return flashcards.generate_flashcards(_text)


        if 'flashcards' not in st.session_state:
            st.session_state.flashcards = get_flashcards(text)

        flashcards_list = st.session_state.flashcards

        if flashcards_list:
            for i, card in enumerate(flashcards_list):
                with st.expander(f"Question {i + 1}", expanded=False):
                    st.write(f"**Q{i + 1}:** {card['question']}")
                    user_ans = st.text_input(f"Your answer for Q{i + 1}:", key=f"ans_{i}")

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button(f"Submit Q{i + 1}", key=f"btn_{i}"):
                            correct = user_ans.strip().lower() == card["answer"].lower()
                            flashcards.update_difficulty(card, correct)
                            if correct:
                                st.session_state[f"result_{i}"] = "correct"
                                st.success("Correct ✅")
                            else:
                                st.session_state[f"result_{i}"] = "wrong"
                                st.error(f"Wrong ❌ | Correct answer: {card['answer']}")
                            st.info(f"Difficulty: {card['difficulty']}")

                    # Show previous result if exists
                    if f"result_{i}" in st.session_state:
                        if st.session_state[f"result_{i}"] == "correct":
                            st.success("✓ You answered this correctly!")
                        else:
                            st.warning(f"Correct answer: {card['answer']}")
        else:
            st.info("No flashcards could be generated for this text.")

    except Exception as e:
        st.error(f"❌ Error generating flashcards: {str(e)}")

    # --- Feedback ---
    st.subheader("📊 Language Feedback")
    try:
        feedback_list = lang_feedback.generate_feedback(text, lang='en')

        if feedback_list:
            st.info("Here are some areas for improvement:")
            for i, f in enumerate(feedback_list):
                with st.expander(f"Feedback #{i + 1}", expanded=False):
                    st.write(f"**Sentence:** {f['sentence']}")
                    st.write(f"**Issue:** {f['issue']}")
                    st.write(f"**Tip:** {f['tip']}")
                    if 'translation_tip' in f:
                        st.write(f"**Tip (Arabic):** {f['translation_tip']}")
                    st.write("---")
        else:
            st.success("🎉 No major language issues detected! Your text looks good!")

    except Exception as e:
        st.error(f"❌ Error generating feedback: {str(e)}")

else:
    st.info("👆 Please upload a PDF, DOCX, or TXT file to get started!")
    st.write("""
    ### Supported file types:
    - **PDF** (.pdf) - Academic papers, articles
    - **Word Documents** (.docx) - Essays, reports  
    - **Text Files** (.txt) - Any plain text content
    """)

# --- Session Management ---
if st.button("🔄 Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("IELTS Study Buddy • Built for effective English learning and practice")