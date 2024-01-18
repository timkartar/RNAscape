// Documentation.js
import './documentation.css';

import React from 'react';
// Import any additional dependencies or styles here
// It outputs highly customizable images that provide insight into RNA tertiary structure.

function Documentation() {

  function scrollToSection(event) {
    event.preventDefault();
    const sectionId = event.target.getAttribute('href').substring(1);
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
  }
  
  return (
  <div className="documentation-container">
      <div className="sidebar">
          <h3>Documentation</h3>
          <a href="#quickstart" onClick={scrollToSection}>Quickstart</a>
          <a href="#uploading-data" onClick={scrollToSection}> Uploading Data</a>
          <a href="#visualizing-data" onClick={scrollToSection}>Visualizing Data</a>
          <a href="#saving-output" onClick={scrollToSection}>Saving Output</a>
          <a href="#advanced-settings" onClick={scrollToSection}>Advanced Settings</a>
          <a href="#bp-annotation" onClick={scrollToSection}>Base Pair Annotation</a>
      </div>
      <div className="documentation">
        <h3 class="centered-h3"><b>RNAscape</b> is a tool for the geometric mapping and customizable 2D visualization of 3D RNA structures.</h3>
        <img class="doc-image" src = "/rnascape/3zp8.svg" alt="Example Output 3zp8"/>
        <h2>Documentation</h2>
        <h3 id="quickstart" class="left-h3">Quickstart</h3>
        <p>To get started, click <b>Run on Example Data</b> in the website header. This runs RNAscape on PDB structure <a href="https://www.rcsb.org/structure/3ZP8">3zp8</a> using your selected settings.</p>
        <p>You can also enter a PDB ID and click <b>Run</b> to run RNAscape on the selected PDB ID.</p>
        <p>Lastly, you can click <a href="/rnascape/3zp8-assembly1.cif" download>Example Input</a> here to download an example input data file.</p>
        <h3 id="uploading-data" class="left-h3">Uploading Data</h3>
        <p>RNAscape supports <b>mmCIF or PDF format file uploads</b>.</p>
        <img class="doc-image" src="/rnascape/upload_file_edited.png" alt="Upload file box"/>
        <p>To load a file for processing, click <b>Browse</b> or drag the file into the browse input box. This may appear differently depending on your operating system and web browser.</p>
        <p>Click <b>Run</b> to generate the 2D visualization for a loaded file or PDB ID.</p>
        <h3 id="visualizing-data" class="left-h3">Visualizing Data</h3>
        <p><b>5'</b> to <b>3'</b> polarity is indicated by the standard black arrows (→) between nucleotides.</p>
        <img class="doc-image" src = "/rnascape/zoom_controls.png" alt="Zoom Controls"/>
        <p>After a structure is visualized, you can manipulate the visualization using:</p>
        <p className="indented">The <b>Rotate Image</b> slider, which alters the rotation of the structure. Simply click <b>Regenerate Plot</b> afterwards to regenerate the graph and text labels in the new orientation.</p>
        <p className="indented">The zoom tools, which allow a user to <b>Zoom In</b>, <b>Zoom Out</b>, <b>Center</b> the graph, and to <b>Reset</b> any previous Zooming/Panning.</p>
        <p>You can also <b>scroll</b> over the image to Zoom In or Zoom Out.</p>
        <p>To <b>pan</b>, click the image and drag with your mouse. This works especially well to visualize parts of larger structures.</p>
        <p><b>Non-WC</b> nucleotides are by default white on the plot. Click <b>Show Log</b> to see more information about them including their DSSR IDs.</p>
        <h3 id="saving-output" class="left-h3">Saving Output</h3>
        <p>Click the <b>Download</b> button to download the RNAscape output image. You can download an <b>SVG</b> or <b>PNG</b>.</p>
        <p>If the image is rotated, RNAscape will generate a rotated PNG or SVG. However, as a best practice, we recommend clicking <b>Regenerate Plot</b> to reprocess and optimize the image.</p>
        <p>Advanced users can click <b>Download</b> and <b>NPZ</b> to download the RNAscape backend output as an <b>NPZ</b> file, which can be opened in Python. This includes the mapped 2D positions for each nucleotide.</p>
        <p>Lastly, users can click <b>Download</b> and <b>Logfile</b> to download the RNAscape log of non-WC nucleotides as a text file.</p>

        <h3 id="advanced-settings" class="left-h3">Loop Bulging and Advanced Settings</h3>
        <p>RNAscape offers many advanced settings to modify the 2D visualization. Click <b>Show Advanced Settings</b> to see all options.</p>
        <p>By default, RNAscape <b>bulges</b> out loops to reduce crowding. Setting <b>Bulge Out Loops</b> to <b>Conditional</b> reduces the size of the graph, but may create more RNA overlap.</p>
        <div className="side-by-side-images">
          <img className="side-image" src="/rnascape/3zp8.svg" alt="Always Loop Bulging"/>
          <img className="side-image" src="/rnascape/3zp8_conditional.svg" alt="Conditional Loop Bulging"/>
        </div>
        <p>The left image depicts <b>Always Bulging</b>. Notice the additional space near residues 18 and 31.</p>
        <p>The right image depicts <b>Conditional Bulging</b>. We recommend experimenting to see what looks best for a given structure.</p>
        <p>Changing the <b>Bulge Out Loops</b> setting changes nucleotide positioning. Therefore, please click <b>Run</b> if you would like to change it for a structure.</p>
        <p>All other settings can be changed for a structure by clicking <b>Regenerate Plot</b>.</p>
        <p>There are three Advanced Settings categories: Nucleotide Settings, Number Settings, and Color Settings.</p>

        <img class="doc-image" src = "/rnascape/nucleotide_settings.png" alt="Nucleotide Settings"/>
        <p><b>Arrow Size</b> modifies how large the arrows are between nucleotides. They can be turned off altogether by setting it to 0, and the default is 1.</p>
        <p><b>Circle Size</b> modifies how large the circles are surrounding each nucleotide. They can be turned off altogether by setting it to 0 (seen below). The default is 1.</p>
        <img class="doc-image" src="/rnascape/no_circle_output.svg" alt="No Circle Output"/>
        <p><b>Circle Label Size</b> modifies how large the text is for each nucleotide. The default is 1.</p>
        <p><b>Base Pair Annotation</b> changes how non-WC base pairing is notated. It is discussed in detail below.</p>
        <img class="doc-image" src="/rnascape/number_settings.png" alt="Residue Numbers Checkbox and Settings"/>
        <p>Check/Uncheck <b>Show Residue Numbers</b> to turn on/off residue numbers. If checked, two additional options are shown:</p>
        <p className="indented"><b>Number Label Size</b> modifies how large the number labels are. The default is 1.</p>
        <p className="indented"><b>Number Distance</b> which changes how far away the number labels are from their corresponding nucleotides. The default is 1.</p>
        <img class="doc-image" src = "/rnascape/select_color_edited.png" alt="Select Color Input"/>
        <p>In Advanced Settings, you can also <b>customize the color</b> of each nucleotide type, either by clicking on the color box, or by inputting a custom hex value. X refers to a non-standard nucleotide.</p>
        <p>Depending on your operating system and web browser, the color selector box may appear differently than the one depicted above.</p>
        <h3 id="bp-annotation" class="left-h3">Base Pair Annotation</h3>
        <p>RNAscape supports three <b>Base Pair Annotation</b> styles, which can be changed in <b>Advanced Settings</b>: Leontis-Westhof, Saenger, and DSSR. You can also select None to remove them altogether.</p>
        <p>The definitions surrounding base pairing can be ambiguous in some cases. All base pairing is calculated via X3DNA-DSSR, which can differ from other methods.</p>
        <p>For the Saenger Base Pair Annotation, there are 28 possible base pair types. For this reason, no legend is provided.</p>
        <p>The Leontis-Westhof Base Pair Annotation Legend has two main parameters</p>
        <p className="indented"><b>c/t</b> refer to a cis or trans bond orientation respectively.</p>
        <p className="indented"><b>W/H/S</b> refer to a Watson-Crick, Hoogsteen, or Sugar edge respectively.</p>
        <p>You can find more information regarding Saenger and Leontis-Westhof Base Pair annotations <a href="https://beta.nakb.org/basics/bases.html">here</a>.</p>
        <p>The DSSR Base Pair Annotation Legend has two main parameters:</p>
        <p className="indented"><b>c/t</b> refer to a cis or trans bond orientation respectively.</p>
        <p className="indented"><b>M/m/W</b> refer to major groove, minor groove, or Watson-Crick edge respectively.</p>
      </div>
  </div>
  );
}

export default Documentation;
