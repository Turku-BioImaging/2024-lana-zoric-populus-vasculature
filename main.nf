workflow {
    imageDataChannel = Channel
        .fromPath("${params.inputDir}/data-list.txt")
        .splitCsv(header: false, sep: ',')
        .map { row -> tuple(clone: row[0], sample: row[1]) }
        .flatten()


    SanitizeFilenames(params.inputDir, imageDataChannel).sampleMeta
        .map { output ->
            def cloneName = output[0].text.trim()
            def sampleName = output[1].text.trim()
            def shapes = output[2]
            def rawImage = output[3]

            return tuple(clone: cloneName, sample: sampleName, shapes: shapes, rawImage: rawImage)
        }
        .flatten()
        .set { sanitizedData }

    GenerateLabelsFromShapes(sanitizedData).sampleMeta
        .collect()
        .set { collectedData }

    GatherMorphologyData(collectedData)
    PlotDistributions(GatherMorphologyData.out.morphologyData)
}

process SanitizeFilenames {
    input:
    path inputDir
    tuple val(clone), val(sample)

    output:
    tuple path('clone-name.txt'), path('sample-name.txt'), path('shapes.csv'), path('raw-image.tif'), emit: sampleMeta

    script:
    """
    python ${params.projectDir}/bin/sanitize_filenames.py \
        --image-path "${params.inputDir}/${clone}/${sample}" \
        --clone "${clone}" \
        --sample "${sample}" \
        --shape-dir "${params.shapeDir}"
    """
}

process GenerateLabelsFromShapes {
    publishDir "${params.outputDir}/clones/${clone}/${sample}", pattern: '*.{tif,csv}', mode: 'copy'

    input:
    tuple val(clone), val(sample), val(shapes), val(rawImage)

    output:
    tuple val(clone), val(sample), path('labels.tif'), emit: sampleMeta
    path 'raw-image.tif'
    path 'shapes.csv'

    script:
    """
    python ${params.projectDir}/bin/generate_labels_from_shapes.py \
        --image-path "${rawImage}" \
        --shapefile-path "${shapes}" \
    """
}

process GatherMorphologyData {
    publishDir "${params.outputDir}", pattern: '*.csv', mode: 'copy'

    input:
    val collectedData

    output:
    path 'morphology-data.csv', emit: morphologyData

    script:
    """
    python ${params.projectDir}/bin/gather_morphology_data.py \
        --data "${collectedData}" \
    """
}

process PlotDistributions {
    publishDir "${params.outputDir}", pattern: "plots", mode: 'copy'

    input:
    path morphologyData

    output:
    path 'plots'

    script:
    """
    python ${params.projectDir}/bin/plot_distributions.py \
        --data "${morphologyData}" 
    """
}
