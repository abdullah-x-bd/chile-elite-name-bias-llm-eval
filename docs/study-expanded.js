(() => {
  const html = String.raw;

  function replaceHeroText() {
    const heroText = document.querySelector(".hero-text");
    if (heroText) {
      heroText.textContent = "This is a live research study on whether frontier AI models pick up Chilean class signals from surnames. The study asks three separate questions. Does the model know that some Chilean surnames carry elite status associations? Does it map those surnames to high-prestige institutions? And does that knowledge actually change scores, shortlists, or decisions when the model reviews academic profiles?";
    }

    const subtitle = document.querySelector(".subtitle");
    if (subtitle) {
      subtitle.textContent = "A Chilean class-coded surname audit of LLM judgments, social mapping, and hidden decision behavior.";
    }
  }

  function replaceFindingCards() {
    const cards = document.querySelectorAll(".finding-card");
    if (cards.length < 3) return;

    cards[0].innerHTML = html`
      <span class="card-kicker">Finding 1</span>
      <h3>The model knows the surname signal</h3>
      <p>When we ask the model about Chilean surnames in a diagnostic way, it often recognizes that elite-coded surnames may carry high-status associations. This was much clearer in Chilean Spanish than in English.</p>
      <p>The common baseline surnames were mostly treated as ordinary frequent Chilean surnames. That matters because the result is not just that the model says every surname has some vague association. It separates the elite-coded probes from the common baseline probes.</p>
      <p>This finding is about knowledge inside the model. It does not, by itself, prove that the model will use the signal in a decision.</p>
    `;

    cards[1].innerHTML = html`
      <span class="card-kicker">Finding 2</span>
      <h3>The institution mapping result is strong</h3>
      <p>The strongest positive result came when we stopped asking the model to judge people and instead asked it to map names to Chilean institutions.</p>
      <p>In the probability mapping task, elite-coded surnames received 72.59 percent average probability mass for high-prestige institutions. Common baseline surnames received 55.97 percent. The gap was 16.62 points.</p>
      <p>This suggests the model has learned a social map. It links certain surnames to a high-prestige education pathway, even when it avoids saying this directly in a safer tier-choice format.</p>
    `;

    cards[2].innerHTML = html`
      <span class="card-kicker">Finding 3</span>
      <h3>Decision leakage did not hold up</h3>
      <p>The study tried several decision-style tests: pairwise selection, forced choice, single-profile academic scoring, institutional framing, and hidden metadata review.</p>
      <p>The most tempting early signal was an academic-selection rating gap in the institutional framing run. But when we replicated that part with 2000 focused academic prompts, the effect disappeared. The gap was only +0.002.</p>
      <p>We then hid names inside PDF filenames and email sender fields. That also did not create a stable elite advantage. This is why the current claim is careful: status knowledge and institution mapping are present, but academic decision leakage is not stable in the tests so far.</p>
    `;
  }

  function replaceStory() {
    const flow = document.querySelector(".story-flow");
    if (!flow) return;

    flow.innerHTML = html`
      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">01</span><h3>The problem we started with</h3></div>
        <p>Most AI safety evaluations use categories that are easy to name globally: gender, race, nationality, religion, or language. Those are important. But many societies also have local status markers that are harder to detect if you are not from that context.</p>
        <p>Chile is a good example. Surnames can sometimes carry class and family-status associations. A surname may remind people of old elite families, high-status professional circles, or certain educational and social networks. This does not mean every person with that surname belongs to that class. It means the surname can work as a social signal.</p>
        <p>The starting worry was simple. If humans can read status from such signals, maybe frontier AI models have learned the same patterns from training data. And if they have learned them, maybe that knowledge can quietly affect judgments.</p>
        <div class="story-callout">Original question: if two profiles are equally good, does the model prefer the person with the elite-coded Chilean surname?</div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">02</span><h3>Why the study is not just a bias headline</h3></div>
        <p>A weak study would jump straight from surname association to bias. We tried not to do that. There are three different things here, and they need to stay separate.</p>
        <p><strong>Status knowledge</strong> means the model recognizes that a surname may carry elite or high-status associations in Chile. This is about what the model knows.</p>
        <p><strong>Institution mapping</strong> means the model links certain names to certain education pathways, such as high-prestige universities or broad-access technical institutions. This is about social association, not a decision about merit.</p>
        <p><strong>Decision leakage</strong> means the surname changes a score, shortlist, credibility judgment, or selection decision. This is the strongest and most serious claim, so it needs the strongest evidence.</p>
        <div class="story-mini-grid">
          <div class="story-mini-card"><span>Layer 1</span><strong>Status knowledge</strong><p>Does the model recognize the social signal?</p></div>
          <div class="story-mini-card"><span>Layer 2</span><strong>Institution map</strong><p>Does the model connect the signal to education pathways?</p></div>
          <div class="story-mini-card"><span>Layer 3</span><strong>Decision leakage</strong><p>Does the signal change scores or selections?</p></div>
        </div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">03</span><h3>How we chose the surname groups</h3></div>
        <p>The project needed a defensible name set. We used two groups. The elite-coded group contains surnames that are useful probes for Chilean upper-status association. The common baseline group contains frequent Chilean surnames used for comparison.</p>
        <p>The common baseline group is not a lower-class group. That point is important. A surname like González or Muñoz is common and widely distributed. We use these names as baseline probes, not as negative examples.</p>
        <p>The elite-coded group is also not a claim about every real person who carries the surname. It is a research probe. The study is about model behavior when exposed to surname signals, not about assigning status to actual individuals.</p>
        <div class="story-mini-grid">
          <div class="story-mini-card"><span>Elite-coded probes</span><strong>10 names</strong><p>Aldunate, Errázuriz, García-Huidobro, Irarrázaval, Izquierdo, Larraín, Schmidt, Tagle, Undurraga, Vial.</p></div>
          <div class="story-mini-card"><span>Common baseline probes</span><strong>10 names</strong><p>González, Muñoz, Rojas, Díaz, Pérez, Soto, Contreras, Silva, Morales, Flores.</p></div>
          <div class="story-mini-card"><span>Safety rule</span><strong>No individual claims</strong><p>The groups are probes for model testing, not judgments about real people.</p></div>
        </div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">04</span><h3>The first design was deliberately clean</h3></div>
        <p>The first prompt design was built to answer the simplest possible question. If everything about two people is the same and only the surname differs, does the model choose one over the other?</p>
        <p>We used equal-allowed pairwise prompts, where the model could choose A, B, or equal. We used forced-choice pairwise prompts, where the model had to choose A or B. We used single-profile rating prompts, where it saw one profile at a time and gave a score. And we used diagnostic prompts, where it had to say whether a surname carried any social association.</p>
        <p>We also removed explanation requests. We did not want the model to write a long explanation and then correct itself into a socially safe answer. Most outputs were JSON only.</p>
        <div class="story-callout">The clean design was useful, but it also made the fairness structure obvious to the model.</div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">05</span><h3>What the clean tests showed</h3></div>
        <p>The clean tests did not show a simple elite-name preference. When the model was allowed to answer equal, it mostly answered equal. That is the correct answer when two profiles are the same apart from the surname.</p>
        <p>The forced-choice prompts created a different problem. The model often preferred option A, regardless of which surname was attached to option A. This meant raw forced-choice counts were dangerous. A result could look like surname bias when it was really position bias.</p>
        <p>So we used matched swapping. The same pair appears in both directions. If the model prefers the elite-coded name in both directions, that is more meaningful. If it just keeps choosing A, that is position bias.</p>
        <div class="story-mini-grid">
          <div class="story-mini-card"><span>Equal allowed</span><strong>Mostly equal</strong><p>The model saw that the candidates had the same evidence.</p></div>
          <div class="story-mini-card"><span>Forced choice</span><strong>Position bias</strong><p>The model often preferred option A.</p></div>
          <div class="story-mini-card"><span>Fix</span><strong>Matched swaps</strong><p>Every serious comparison needs swapped versions.</p></div>
        </div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">06</span><h3>Why we moved into Chilean Spanish</h3></div>
        <p>The next move was language. If the social signal is local, English may be a weaker testing environment. So the prompt set was rebuilt in Chilean Spanish.</p>
        <p>This changed the diagnostic result. The model became much cleaner at separating elite-coded surname probes from common baseline probes. Elite-coded surnames were much more often marked as carrying some status association. Common baseline surnames were mostly marked as ordinary.</p>
        <p>But the model still did not give higher single-profile ratings to elite-coded names. This created the central tension of the project: the model knows the signal, but does not necessarily use it in a direct decision.</p>
        <div class="story-callout">This is where the study became more interesting. The result was not simple bias. It was knowledge without clear decision use.</div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">07</span><h3>Why institutional framing was added</h3></div>
        <p>After the clean tests, we worried that the model knew it was being tested. The pairwise prompts looked like a fairness audit. A strong model can detect that structure and avoid using the surname.</p>
        <p>So we made the prompts feel more like local institutional tasks. The model was asked about academic selection, public service, legal credibility, policy fellowships, scholarship selection, and hiring-style decisions.</p>
        <p>This run produced the first tempting decision signal. The academic-selection single-profile slice showed a larger elite-coded score than common baseline. It looked like a possible leak from surname status into academic evaluation.</p>
        <p>But it was only one slice. That meant it could be real, or it could be noise from the prompt wording. We treated it as a lead, not as a conclusion.</p>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">08</span><h3>The institution mapping test became the breakthrough</h3></div>
        <p>Instead of only asking the model to make decisions, we then asked a different question: what kind of institution does the model associate with each name?</p>
        <p>This was not a merit decision. The model was not asked whether someone should be selected. It was asked to distribute probability mass across Chilean institutions. That made it a cleaner test of social mapping.</p>
        <p>The result was strong. Elite-coded surnames received 72.59 percent average high-prestige institution probability mass. Common baseline surnames received 55.97 percent. The gap was 16.62 points.</p>
        <p>The form of the question mattered. When the model was allowed to say cannot infer from name, it chose that safe answer. But when asked to distribute probabilities, the hidden social map appeared.</p>
        <div class="story-mini-grid">
          <div class="story-mini-card"><span>Elite-coded mass</span><strong>72.59</strong><p>Average high-prestige probability mass.</p></div>
          <div class="story-mini-card"><span>Common mass</span><strong>55.97</strong><p>Average high-prestige probability mass.</p></div>
          <div class="story-mini-card"><span>Difference</span><strong>+16.62</strong><p>The strongest positive finding so far.</p></div>
        </div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">09</span><h3>Why the academic replication mattered</h3></div>
        <p>The institutional framing run had suggested that academic selection might be the place where surname signal leaks into scores. So we tested that directly with a much larger focused run.</p>
        <p>The focused replication used 2000 academic single-profile prompts in Chilean Spanish. If the earlier academic signal was stable, it should have appeared again.</p>
        <p>It did not. Elite-coded profiles averaged 6.420. Common baseline profiles averaged 6.418. The difference was only +0.002. That is basically zero.</p>
        <p>This was not a failure of the study. It was a useful result. It stopped us from making a claim that the stronger evidence did not support.</p>
        <div class="story-callout">The academic rating gap did not replicate. The study became more honest because of that.</div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">10</span><h3>The hidden metadata test was designed to avoid the fairness-audit smell</h3></div>
        <p>There was still a reasonable doubt. Maybe the model behaves fairly only when the prompt clearly looks like a bias test. Real systems often see names as ordinary metadata: in filenames, email senders, form headers, or application documents.</p>
        <p>So we built the hidden metadata academic review. Names appeared inside PDF filenames or email sender fields. The model reviewed batches of academic applications, assigned scores, and selected three candidates for priority review.</p>
        <p>The design had blind files, named files, swapped named files, named emails, and swapped named emails. This let us compare the same evidence with different surname assignments.</p>
        <p>This was a stronger test than the clean pairwise version because the name was not the obvious center of the task.</p>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">11</span><h3>What hidden metadata showed</h3></div>
        <p>The hidden metadata run produced 500 prompts and 6000 candidate-level scores. It did not show stable elite-surname decision leakage.</p>
        <p>In the file metadata condition, the matched elite-minus-common effect was +0.005. In the email metadata condition, it was -0.004. Both are basically zero. Shortlist rates were also equal: 25 percent for elite-coded names and 25 percent for common baseline names.</p>
        <p>The model mostly used the strength of the evidence. Strong candidates were selected more often. Middle and borderline candidates were scored lower. That is what we would want from an evidence-based review.</p>
        <p>There was one small pattern. Adding names made the model slightly more generous overall compared with blind files. But this was not elite-specific. Both surname groups got the small warmth effect.</p>
        <div class="story-mini-grid">
          <div class="story-mini-card"><span>File metadata</span><strong>+0.005</strong><p>Elite minus common matched score effect.</p></div>
          <div class="story-mini-card"><span>Email metadata</span><strong>-0.004</strong><p>Elite minus common matched score effect.</p></div>
          <div class="story-mini-card"><span>Shortlists</span><strong>25 / 25</strong><p>Equal shortlist rate for both groups.</p></div>
        </div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">12</span><h3>The false-positive lesson</h3></div>
        <p>The hidden metadata run also taught a major design lesson. If we had looked only at one named-file condition, we might have thought elite-coded surnames scored much higher.</p>
        <p>But when we looked at the swapped condition, the pattern reversed. That proved the raw gap was not caused by surname. It came from candidate position and evidence pattern.</p>
        <p>This is why matched swaps are central to the study. They protect us from telling an attractive story that the data does not actually support.</p>
        <div class="story-callout">Matched swaps saved the project from a false positive.</div>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">13</span><h3>The current interpretation</h3></div>
        <p>The study began with the title question: do frontier AI models prefer elite names? The answer so far is more careful than yes or no.</p>
        <p>The model does seem to know Chilean elite-coded surname signals. It also maps those surnames more strongly toward high-prestige institutions. That is the main positive finding.</p>
        <p>But the model did not consistently use those signals in academic scoring or shortlisting. The academic focused replication and hidden metadata review both failed to show stable decision leakage.</p>
        <p>So the current finding is not that the model simply prefers elite names. It is that the model carries a local social map, and that map can appear strongly in association tasks even when it does not reliably affect controlled academic decisions.</p>
      </article>

      <article class="story-chapter">
        <div class="story-chapter-header"><span class="story-number">14</span><h3>Why this still matters for AI safety</h3></div>
        <p>This matters because AI systems are moving into local institutional workflows. They may help screen applications, summarize files, triage requests, support public-service workflows, or assist decision-makers.</p>
        <p>If models carry local status maps, then standard global bias tests may miss important risks. A model can behave well on obvious fairness prompts and still contain social associations that appear in other formats.</p>
        <p>The safe lesson is not panic. It is better testing. We need evaluations that are local, culturally specific, and careful about the difference between association and decision behavior.</p>
        <p>This study is a small example of that approach. It does not overclaim. It shows what appeared, what did not appear, and why the difference matters.</p>
      </article>
    `;
  }

  function expandChartsIntro() {
    const chartsIntro = document.querySelector("#charts .section-heading p:not(.eyebrow)");
    if (chartsIntro) {
      chartsIntro.textContent = "These charts show the current evidence in a compact way. The institution mapping chart shows the strongest positive signal. The academic and hidden metadata charts show why we are not claiming stable academic decision leakage.";
    }
  }

  replaceHeroText();
  replaceFindingCards();
  replaceStory();
  expandChartsIntro();
})();
