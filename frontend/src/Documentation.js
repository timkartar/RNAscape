// Documentation.js
import './documentation.css';

import React from 'react';
// Import any additional dependencies or styles here

function Documentation() {
  return (
    <div className="documentation">
      <h2>Documentation</h2>
      <p><b>RNAScape</b> is a tool for the <b>visualization</b> of <b>RNA secondary structure</b>. It outputs highly <b>customizable</b> images that provide insight into RNA <b>tertiary structure</b>.</p>
      <h3>Quickstart</h3>
      <p>To quickly get started, click <b>Load Example Data</b>. This runs RNAScape on PDB structure 3zp8 using the selected settings.</p>
      <p>You can also click <b>Download Example Data</b> to see an example input data file.</p>
      <h3>Uploading Data</h3>
      <p>RNAScape supports <b>CIF file uploads</b>, which can include other nucleic acids or proteins. Only the RNA will be visualized.</p>
      <p>To upload a file for processing, click <b>Browse</b> or drag the file into the browse input box.</p>
      <p>You can select a specific <b>Base Pair Annotation</b>, including Leontis-Westhof, Saenger, and DSSR.</p>
      <p>By default, RNAScape <b>conditionally bulges</b> out loops, depending on how crowded the graph is. Setting <b>Loop Bulging</b> to <b>Always</b> creates less overlap, but may increase the size of the graph.</p>
      <h3>Visualizing Data</h3>
      <p><b>5'</b> to <b>3'</b> polarity is indicated by the standard black arrows between nucleotides.</p>
      <p>After a structure is visualized, a user can manipulate the structure using:</p>
      <p className="indented">The <b>rotation slider</b>, which is a simple slider altering the rotation of the structure. Simply click <b>Regenerate Labels</b> afterwards to regenerate the labels in the correct orientation.</p>
      <p className="indented">The zoom tools, which allow a user to <b>Zoom In</b>, <b>Zoom Out</b>, <b>Center</b> the graph, and to <b>Reset</b> any previous Zooming/Panning</p>
      <p>You can also <b>scroll</b> over the image to Zoom In or Zoom Out.</p>
      <p>To <b>pan</b> the image, click on the image and drag with your mouse. This works especially well to visualize parts of larger structures.</p>
      <h3>Saving Output</h3>
      <p>Click the <b>Download</b> button to download the RNAScape output image.</p>
    </div>
  );
}

export default Documentation;