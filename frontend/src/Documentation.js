// Documentation.js
import './documentation.css';

import React from 'react';
// Import any additional dependencies or styles here
// It outputs highly customizable images that provide insight into RNA tertiary structure.

function Documentation() {
  return (
    <div className="documentation">
      <h3><b>RNAscape</b> is a tool for the geometric mapping and customizable 2D visualization of 3D RNA structures.</h3>
      <img class="doc-image" src = "/rnascape/3zp8.svg" alt="Example Output 3zp8"/>
      <h2>Documentation</h2>
      <h3>Quickstart</h3>
      <p>To get started, click <b>Run on Example Data</b>. This runs RNAscape on PDB structure <a href="https://www.rcsb.org/structure/3ZP8">3zp8</a> using your selected settings.</p>
      <p>You can also click <b>Example Input</b> in the above header to download an example input data file.</p>
      <h3>Uploading Data</h3>
      <p>RNAscape supports <b>mmCIF or PDF format file uploads</b>, which should contain nucleic acids with at least one helical segment.</p>
      <img class="doc-image" src="/rnascape/upload_file_edited.png" alt="Upload file box"/>
      <p>To load a file for processing, click <b>Browse</b> or drag the file into the browse input box. This may appear different depending on your operating system and web browser.</p>
      <p>You can select a specific <b>Base Pair Annotation</b>, including Leontis-Westhof, Saenger, and DSSR.</p>
      <p>Click <b>Run</b> to generate the 2D visualization for a loaded file.</p>
      <h3>Visualizing Data</h3>
      <p><b>5'</b> to <b>3'</b> polarity is indicated by the standard black arrows (→) between nucleotides.</p>
      <img class="doc-image" src = "/rnascape/zoom_controls_edited.png" alt="Zoom Controls"/>
      <p>After a structure is visualized, you can manipulate the visualization using:</p>
      <p className="indented">The <b>Rotate Image</b> slider, which alters the rotation of the structure. Simply click <b>Regenerate Labels</b> afterwards to regenerate residue labels in the new orientation.</p>
      <p className="indented">The zoom tools, which allow a user to <b>Zoom In</b>, <b>Zoom Out</b>, <b>Center</b> the graph, and to <b>Reset</b> any previous Zooming/Panning.</p>
      <p>You can also <b>scroll</b> over the image to Zoom In or Zoom Out.</p>
      <p>To <b>pan</b>, click the image and drag with your mouse. This works especially well to visualize parts of larger structures.</p>
      <h3>Saving Output</h3>
      <p>Click the <b>Download</b> button to download the RNAscape output image. You can download an <b>SVG</b> or <b>PNG</b>.</p>
      <p>If the image is rotated, RNAscape will generate a rotated PNG or SVG. However, as a best practice, we recommend clicking <b>Regenerate Labels</b> to reprocess and optimize the image.</p>
      <h3>Advanced Settings</h3>
      <p>RNAscape offers many advanced settings to modify the 2D visualization. Click <b>Show Advanced Settings</b> to see all options.</p>
      <p>By default, RNAscape <b>bulges</b> out loops to reduce crowding. Setting <b>Loop Bulging</b> to <b>Conditional</b> reduces the size of the graph, but may create more RNA overlap</p>
      <div className="side-by-side-images">
        <img className="side-image" src="/rnascape/3zp8.svg" alt="Always Loop Bulging"/>
        <img className="side-image" src="/rnascape/3zp8_conditional.svg" alt="Conditional Loop Bulging"/>
      </div>
      <p>The left image depicts <b>Always Bulging</b>. Notice the additional space near residues 18 and 31.</p>
      <p> The right image depicts <b>Conditional Bulging</b>. We recommend experimenting to see what looks best for a given structure.</p>
      <img class="doc-image" src = "/rnascape/circle_arrow_settings_edited.png" alt="Marker Settings"/>
      <p><b>Arrow Size</b> modifies how large the arrows are between nucleotides. They can be turned off altogether by setting it to 0, and the default is 1.</p>
      <p><b>Circle Size</b> modifies how large the circles are surrounding each nucleotide. They can be turned off altogether by setting it to 0 (seen below). The default is 1.</p>
      <img class="doc-image" src="/rnascape/no_circle_output.svg" alt="No Circle Output"/>
      <p><b>Circle Label Size</b> modifies how large the text is for each nucleotide. The default is 1.</p>
      <img class="doc-image" src="/rnascape/residue_numbers_edited.png" alt="Residue Numbers Checkbox and Settings"/>
      <p>Check/Uncheck <b>Show Residue Numbers</b> to turn on/off residue numbers. If checked, two additional options are shown:</p>
      <p className="indented"><b>Number Label Size</b> modifies how large the number labels are. The default is 1.</p>
      <p className="indented"><b>Number Distance</b> which changes how far away the number labels are from their corresponding nucleotides. The default is 1.</p>
      <img class="doc-image" src = "/rnascape/select_color_edited.png" alt="Select Color Input"/>
      <p>In Advanced Settings, you can also <b>customize the color</b> of each nucleotide type, either by clicking on the color box, or by inputting a custom hex value. X refers to a non-standard nucleotide.</p>
      <p>Depending on your operating system and web browser, the color selector box may appear different than the one depicted above.</p>
      <h3>Base Pair Annotation</h3>
      <p>Helices and base pairing are detected using X3DNA-DSSR.</p>
      <p>The definitions surrounding base pairing can be ambiguous in some cases. All base pairing is calculated via X3DNA-DSSR, which can differ from other methods.</p>
      <p>For the Saenger Base Pair Annotation, there are 28 possible base pair types. No legend is provided.</p>
      <p>For the Leontis-Westhof Base Pair Annotation, bonds are delineated by both bond orientation and interacting edges.</p>
      <p>You can find more information regarding Saenger and Leontis-Westhof Base Pair annotations <a href="https://beta.nakb.org/basics/bases.html">here</a>.</p>
      <p>The DSSR Base Pair Annotation is similar to Leontis-Westhof; however, each bond only contains one symbol type.</p>
    </div>
  );
}

export default Documentation;
